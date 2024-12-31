from flask import Flask, abort, render_template, request, redirect, send_from_directory
import requests
from flask_basicauth import BasicAuth
import json
import os
import modules.stringutils as sutil
import modules.datautils as dutil
from datetime import date
import configparser
import sqlite3

VERSION = "v0.02.1beta"
INTERNALVERSION = 21
datapath = dutil.datapath
passchangemsg = ""

conn = sqlite3.connect("app/files.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS files (
                id integer primary key,
                filename text not null,
                description text,
                upload_date text not null,
                uuid integer unique not null
                );
               """)

def create_app():
    if not os.path.exists(datapath):
        os.makedirs(datapath)

    config = configparser.ConfigParser()
    if not os.path.isfile("app/config.ini"):
        config['settings'] = {
        'USERNAME': "admin",
        'PASSWORD': "admin",
        'CHECK-FOR-UPDATES' : "no"
        }
        with open('app/config.ini', 'w') as configfile:
            config.write(configfile)

    config.read('app/config.ini')
    USERNAME = str(config.get('settings', 'username'))
    PASSWORD = str(config.get('settings', 'password'))
    HOST = '0.0.0.0'
    PORT = 6798
    CHKFORUPDATES = str(config.get('settings', 'check-for-updates'))

    if CHKFORUPDATES == "yes":
        response = requests.get(f'https://codeberg.org/api/v1/repos/m3r/busfs-server/releases')
        release = response.json()
        if response.status_code == 200:
            if len(release) > 0 and str(release[0]['tag_name']) != VERSION:
                versionmessage = f'Your version is "{VERSION}", and the latest version is "{str(release[0]["tag_name"])}".'
            else:
                versionmessage = "You are running the latest version of this app"
        else:
            versionmessage = f'Something went wrong while checking for updates. Response code is {int(response.status_code)}. Your version is "{VERSION}" and the upstream is "{str(release[0]["tag_name"])}"'
    else:
        versionmessage = ""

    app = Flask(__name__)

    app.config['BASIC_AUTH_USERNAME'] = USERNAME
    app.config['BASIC_AUTH_PASSWORD'] = PASSWORD
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)

    if not os.path.exists(datapath):
        os.makedirs(datapath)

    @app.route("/")
    def index():
        global passchangemsg
        filelists = dutil.loadData()
        return render_template("index.html", filelists = filelists, versionmessage=versionmessage, passchangemsg = passchangemsg)

    @app.post("/upload-file")
    def upload():

        file = request.files['userfile']
        if file == None:
            abort(400)

        desc = request.form['userdescription']

        randstr = sutil.randomTen()

        while os.path.isdir(os.path.join(datapath, randstr)):
            randstr = sutil.randomTen()

        os.makedirs(os.path.join(datapath, randstr))
        file.save(f'{datapath}/{randstr}/{file.filename}')
        today = date.today()
        todayformat = today.strftime("%d.%m.%Y")

        dutil.addFileToDB(file, desc, todayformat, randstr)

        return redirect("/")

    @app.route('/download/<uuid>')
    def download(uuid):
        return send_from_directory(f"{datapath}/{uuid}", dutil.getFile(uuid, ), as_attachment=True)

    @app.route("/delete/<uuid>")
    def delete(uuid):
        dutil.delDir(uuid, )
        return redirect("/")

    @app.post('/update-description/<uuid>')
    def update(uuid):
        desc = request.form['inlinedesc']
        dutil.updateDesc(uuid, desc)
        return redirect("/")

    @app.post('/update-creds')
    def changecreds():
        global passchangemsg
        newuser = request.form['newuser']
        if newuser:
            config.set('settings', 'username', str(newuser))
            with open('app/config.ini', 'w') as configfile:
                config.write(configfile)
        newpass = request.form['newpass']
        if newpass:
            config.set('settings', 'password', str(newpass))
            with open('app/config.ini', 'w') as configfile:
                config.write(configfile)
        if newpass or newuser:
            passchangemsg = "Your credentials have been changed. Please restart the server."
        return redirect("/")


    ### API

    # @app.get("/v1/uploaded")
    # def apihome():
    #     return dutil.jsonLoad()
    

    #app.run(debug=True, host= HOST, port=PORT) # UNCOMMENT FOR DEVEL

    return app

#create_app() # UNCOMMENT FOR DEVEL
