

# Function to generate a QR code for an Ethereum address
def generate_qr_code(ethereum_address, filename='qr.png'):
    import qrcode
    import cv2
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(ethereum_address)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("static\\"+filename)

# Function to decode a QR code and retrieve the Ethereum address
def decode_qr_code(qr_code_image):
    import cv2
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(qr_code_image)

    if retval:
        ethereum_address = decoded_info[0]
        return ethereum_address
    else:
        return None


'''
# Ethereum address to encode and decode
ethereum_address = "0x292435996Ff963D305bbbb479D319B12A062Ed34"

# Generate a QR code
generate_qr_code(ethereum_address, "ethereum_address_qr.png")
print(f"QR code for Ethereum address '{ethereum_address}' generated.")

# Decode the QR code and retrieve the Ethereum address
decoded_ethereum_address = decode_qr_code(cv2.imread("ethereum_address_qr.png"))

if decoded_ethereum_address:
    print(f"Decoded Ethereum address: {decoded_ethereum_address}")
else:
    print("QR code decoding failed.")'''
