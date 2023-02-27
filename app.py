from flask import Flask, render_template, request, abort, send_file, redirect, send_from_directory, url_for
from flask_basicauth import BasicAuth
import json
import os
import stringutils as sutil
import datautils as dutil
from datetime import date
from shutil import rmtree
import configparser

VERSION = "v0.01.0beta"

config = configparser.ConfigParser()
if not os.path.isfile("config.ini"):
    config['settings'] = {
    'USERNAME': sutil.randomTen(),
    'PASSWORD': sutil.randomTen(),
    'HOST': '0.0.0.0',
    'PORT': '6798',
    'CHECK-FOR-UPDATES' : "yes" if input("Do you want to check for updates automatically? y/N ") in ["y", "Y", "yes"] else "no"
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

##############################
#           CONFIG           # !!!!!!! PLEASE CHANGE YOUR DEFAULT USERNAME AND PASSWORD !!!!!!!
USERNAME = "admin"           # The username you wish to use. Please put it in quotation marks
PASSWORD = "admin"           # The password you wish to use. Please put it in quotation marks as well
HOST = "0.0.0.0"             # Put in the IP address that you wish to listen from. This one also goes in quotation marks
PORT = 6798                  # Put in the port number that you wish to listen from. This one does not go in quotation marks.
#LOG_LEVEL = ""              #
##############################

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = USERNAME
app.config['BASIC_AUTH_PASSWORD'] = PASSWORD
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)
datapath = 'data'

if not os.path.exists(datapath):
    os.makedirs(datapath)

@app.route("/")
def index():
    fileNamesList, descriptionList, uploadDateList, uuidList = dutil.loadData()
    return render_template("index.html", fileNamesList=fileNamesList, descriptionList=descriptionList, uploadDateList=uploadDateList, uuidList=uuidList)

@app.post("/upload-file")
def upload():

    file = request.files['userfile']
    if file == None:
        return("400", 400)

    desc = request.form['userdescription']

    randstr = sutil.randomFour()

    while os.path.isdir(randstr):
        randstr = sutil.randomFour()

    os.makedirs(f"{datapath}/{randstr}")
    file.save(f'{datapath}/{randstr}/{file.filename}')
    today = date.today()
    todayformat = today.strftime("%d.%m.%Y")
    jsontowrite = {
        "file_name": file.filename,
        "date_uploaded": todayformat,
        "description": desc,
        "uuid": randstr,
    }
    with open(f'{datapath}/{randstr}/data.json', 'w') as f:
        json.dump(jsontowrite, f)

    return redirect("/")

@app.route('/download/<uuid>')
def download(uuid):
    return send_from_directory(f"data/{uuid}", dutil.getFile(uuid), as_attachment=True)

@app.route("/delete/<uuid>")
def delete(uuid):
    rmtree(dutil.getDir(uuid))
    return redirect("/")

@app.post('/update-description/<uuid>')
def update(uuid):
    desc = request.form['inlinedesc']
    dutil.updateDesc(uuid, desc)
    return redirect("/")

app.run(debug=True, host= HOST, port=PORT)
