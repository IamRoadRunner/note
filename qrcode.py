import base64
import qrcode

def url2qrcode(data):
    '''
    二维码
    '''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )
    qr.add_data(data)
    img = qr.make_image()
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    return base64.b64encode(image_stream)
