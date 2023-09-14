import os
import gitmodules

from flask import Flask, render_template, flash, request, redirect, url_for, logging, make_response
from werkzeug.utils import secure_filename
from meca.src.main import api

UPLOAD_FOLDER = 'storage'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
logging.create_logger(app)

@app.route('/')
def landing():  # put application's code here
    lib_key = request.cookies.get("lib-key")
    lib_id = request.cookies.get("lib-id")

    lib_key_cookie = False if lib_key else True
    lib_id_cookie = False if lib_id else True

    # Need to add a security layer
    return render_template("main.html", lib_key=lib_key_cookie, lib_id=lib_id_cookie)


@app.route('/', methods=['POST'])
def landing_input():
    # Check and Set Lib Key Cookies
    LIB_KEY = request.form.get("lib-key")
    if LIB_KEY:
        app.logger.info(f'{LIB_KEY}')
        res = make_response(redirect(url_for('landing')))
        res.set_cookie("lib-key", LIB_KEY)
        return res

    LIB_ID = request.form.get("lib-id")
    if LIB_ID:
        app.logger.info(f'{LIB_ID}')
        res = make_response(redirect(url_for('landing')))
        res.set_cookie("lib-id", LIB_ID)
        return res

    # Check and Set Files
    input_files = request.files.getlist('file[]')
    if not input_files: return redirect(url_for('landing'))
    files = []

    for file in input_files:
        if not allowed_file(file.filename): continue
        filename = secure_filename(file.filename)

        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(path)
        file.save(path)
        files.append(path)

    if files:
        api(files, LIB_KEY, LIB_ID)

    return redirect(url_for('landing'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
