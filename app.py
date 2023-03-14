from flask import Flask, render_template, request, redirect, send_from_directory
import requests
from flask_basicauth import BasicAuth
import json
import os
import stringutils as sutil
import datautils as dutil
from datetime import date
from shutil import rmtree
import configparser

VERSION = "v0.02.0beta"

def create_app():
    config = configparser.ConfigParser()
    if not os.path.isfile("config.ini"):
        config['settings'] = {
        'USERNAME': sutil.randomTen(),
        'PASSWORD': sutil.randomTen(),
        #'HOST': '0.0.0.0', Enable for debugging purposes for when using the built in flask server
        #'PORT': '6798',
        'CHECK-FOR-UPDATES' : "no"
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    config.read('config.ini')
    USERNAME = str(config.get('settings', 'username'))
    PASSWORD = str(config.get('settings', 'password'))
    #HOST = str(config.get('settings', 'host'))
    #PORT = int(config.get('settings', 'port'))
    CHKFORUPDATES = str(config.get('settings', 'check-for-updates'))

    if CHKFORUPDATES == "yes":
        response = requests.get(f'https://codeberg.org/api/v1/repos/m3r/busfs-server/releases')
        release = response.json()
        if response.status_code == 200:
            if len(release) > 0 and str(release[0]['tag_name']) != VERSION:
                versionmessage = f'Your version is "{VERSION}", and the latest version is "{str(release[0]["tag_name"])}".' #print(f'Your version is {VERSION}, and the latest version is {str(release[0]["tag_name"])}.')
            else:
                versionmessage = "You are running the latest version of this app" #print(f'You are running the latest version of this app')
        else:
            versionmessage = f'Something went wrong while checking for updates. Response code is {int(response.status_code)}. Your version is "{VERSION}" and the upstream is "{str(release[0]["tag_name"])}"' #print(f'Something went wrong while checking for updates. Response code is {int(response.status_code)}. Your version is {VERSION} and the upstream is {str(release[0]["tag_name"])}')
    else:
        versionmessage = ""

    datapath = 'data'
    
    app = Flask(__name__)

    app.config['BASIC_AUTH_USERNAME'] = USERNAME
    app.config['BASIC_AUTH_PASSWORD'] = PASSWORD
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)

    if not os.path.exists(datapath):
        os.makedirs(datapath)

    @app.route("/")
    def index():
        fileNamesList, descriptionList, uploadDateList, uuidList = dutil.loadData()
        return render_template("index.html", fileNamesList=fileNamesList, descriptionList=descriptionList, uploadDateList=uploadDateList, uuidList=uuidList, versionmessage=versionmessage)

    @app.post("/upload-file")
    def upload():

        file = request.files['userfile']
        if file == None:
            return("400", 400)

        desc = request.form['userdescription']

        randstr = sutil.randomTen()

        while os.path.isdir(randstr):
            randstr = sutil.randomTen()

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

    #app.run(debug=True, host= HOST, port=PORT)

    return app

#create_app()
