import os.path

from qrcodegenerator import create_qr_code_image
from config import Config

from flask import Flask, send_file, request

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index_get():
    form = '<h1>Make a QR Code</h1><form method="POST" action="/"> \
                <label for="qrurl">QR URL:</label><br> \
                <input type="text" id="qrurl" name="qrurl" value="http://njit.edu"><br> \
                <input type="submit" value"Submit"> \
            </form>'

    return form


@app.route("/", methods=['POST'])
def index_post():
    full_path = os.getcwd()
    qr_url = request.form.get("qrurl")
    qr_file_name = request.form.get("qr_file_name")

    directory_path_and_file_name = os.path.join(full_path, Config.QR_CODE_IMAGE_DIRECTORY,
                                                Config.QR_CODE_DEFAULT_FILE_NAME)

    qr_image = create_qr_code_image(qr_url)
    for i in range(0, 1):
        while True:
            try:
                qr_image.save(directory_path_and_file_name)
            except FileNotFoundError:
                qr_image_directory = Config.QR_CODE_IMAGE_DIRECTORY
                new_directory_path = os.path.join(full_path, qr_image_directory)
                os.mkdir(new_directory_path)
                continue
            break
    return send_file(directory_path_and_file_name, mimetype='image/png')
