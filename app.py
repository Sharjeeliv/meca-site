from flask import Flask, render_template, flash, request, redirect, url_for, logging

import os

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER
logging.create_logger(app)


@app.route('/')
def home():  # put application's code here
    app.logger.info("Activated")
    return render_template("main.html")


@app.route('/', methods=['POST'])
def upload_file():
    app.logger.info("Activated")
    files = request.files.getlist('file[]')
    for file in files:
        print(file.filename)
    # print(request.files)
    # if uploaded_file.filename != '':
    #     # uploaded_file.save(uploaded_file.filename)
    #     uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename))
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
