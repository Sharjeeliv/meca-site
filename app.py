import os
import gitmodules

from flask import Flask, render_template, flash, request, redirect, url_for, logging, make_response
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = 'storage'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
logging.create_logger(app)


@app.route('/')
def landing():  # put application's code here
    cookie_input = False if request.cookies.get("lib-key") else True
    # Need to add a security layer
    return render_template("main.html", cookie_input=cookie_input)

@app.route('/', methods=['POST'])
def landing_input():

    # Check and Set Lib Key Cookies
    text = request.form.get("cookie")
    if text:
        app.logger.info(f'{text}')
        res = make_response(redirect(url_for('landing')))
        res.set_cookie("lib-key", text)
        return res

    # Check and Set Files
    input_files = request.files.getlist('file[]')
    if not input_files: return redirect(url_for('landing'))
    files = []

    for file in input_files:
        if not allowed_file(file.filename): continue
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        files.append(path)

    return redirect(url_for('landing'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
