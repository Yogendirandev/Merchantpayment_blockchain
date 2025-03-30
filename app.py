from flask import Flask, request, send_file, make_response, url_for, render_template, flash, session, redirect
import db_conns
from web3 import Web3, exceptions
import qr_gen

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def Login():
    return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        lis = db_conns.login(username, password)
        if len(lis) > 0:
            return redirect(url_for('home')+f"?username={username}")
        else:
            flash("Login failed, Check your credentials...")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        priv_key = request.form['priv_key']
        acc_addr = request.form['acc_addr']
        db_conns.signup(username, acc_addr, priv_key, password)
        flash("Account Created Successfully...")
    return redirect(url_for('login'))


@app.route('/home',methods=["GET", "POST"])
def home():
    username = request.args.get('username').replace("'", "")
    
    print("username is: -----------------------: ",username)
    priv_key = db_conns.getPrivateKey(username)
    acc_addr = db_conns.getAccountAddress(username)
    return render_template("home.html", user = username, address = acc_addr, privateKey = priv_key)

@app.route('/sendEth', methods=["GET", "POST"])
def sendEth():
    username = request.form['username']
    priv_key = db_conns.getPrivateKey(username)
    from_acc = db_conns.getAccountAddress(username)
    
    
    #amount = request.form['amount']
    
    return render_template("sendEth.html", user = username, address = from_acc, privateKey = priv_key)

@app.route('/sentMsg', methods=["GET", "POST"])
def sentMsg():
    username = request.form['username']
    priv_key = db_conns.getPrivateKey(username)
    from_acc = db_conns.getAccountAddress(username)
    
    if('Amount' in request.form.keys()):
        amount = request.form['Amount']
        to_acc = request.form['ReceiverAddress']
        url = "HTTP://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(url))
        nonce = web3.eth.get_transaction_count(from_acc)

        #Build the Transaction:
        tx = {
            'nonce': nonce,
            'to': to_acc,
            'value': web3.to_wei(amount, 'ether'),
            'gas': 2_000_000,
            'gasPrice': web3.to_wei('50', 'gwei')
        }
        message = ""
        try:
            signed_tx = web3.eth.account.sign_transaction(tx, priv_key)
            tx_hash = (web3.eth.send_raw_transaction(signed_tx.rawTransaction))
            tx_hash = web3.to_hex(tx_hash)
            message = "Sent Successfully!!!"
        except ValueError:
            message = "Insufficient Funds!!!"
            tx_hash = "---"
        except exceptions.InvalidAddress as e:
            message = "Invalid Sender Address: "+e.args[0].split(" ")[-1][1:-1]
            tx_hash = "---"
        except TypeError as e:
            error_message = str(e)
            start = error_message.find("'to': '") + 6
            end = error_message.find("'", start)
            address = error_message[start:end]
            message = "Invalid Receiver Address: "+address
            tx_hash = "---"
        return render_template("sentMsg.html", message = message
                               ,username = username, s_addr = from_acc, r_addr = to_acc, amt = amount, txn_hash=tx_hash
                               
                               )

@app.route('/receiveEth',methods=["GET", "POST"])
def receiveEth():
    username = request.form['username']
    from_acc = db_conns.getAccountAddress(username)
    qr_gen.generate_qr_code(from_acc)
    return render_template('receiveEth.html', addr = from_acc, username=username)

@app.route('/checkBalance',methods=["GET", "POST"])
def checkBalance():
    username = request.form['username']
    url = "HTTP://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(url))
    address = db_conns.getAccountAddress(username)
    balance_wei = web3.eth.get_balance(address)
    balance_ether = web3.from_wei(balance_wei, 'ether')
    return render_template('checkBalance.html', addr = address, bal = balance_ether)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5002, debug=True)