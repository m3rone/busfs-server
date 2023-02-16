from flask import Flask, render_template, request, abort, send_file, redirect, url_for
from flask_basicauth import BasicAuth
import json
import os
import stringutils as sutil
import datautils as dutil
from datetime import date
import glob
from shutil import rmtree

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
    
@app.route("/upload-file", methods=['POST'])
def upload():
    #filename = ""
    file = request.files['file']
    if file == None:
        return("400", 400)
    
    desc = request.form.get('data')
    if desc == None:
        return ("400", 400)
    
    filenamewex = file.filename
    if filenamewex is not None: # second None check just to escape my pyright error
        global filenamewoex
        filenamewoex, ext = os.path.splitext(filenamewex)
        
    desc = json.loads(desc)['desc']
    randstr = sutil.randomFour()
    dirname = filenamewoex + "-" + randstr
    os.makedirs(f"{datapath}/{dirname}")
    file.save(f'{datapath}/{dirname}/{filenamewex}')
    today = date.today()
    todayformat = today.strftime("%d.%m.%Y")
    jsontowrite = {
        "file_name": filenamewex,
        "date_uploaded": todayformat,
        "description": desc,
        "uuid": randstr,
    }
    with open(f'{datapath}/{dirname}/data.json', 'w') as f:
        json.dump(jsontowrite, f)
    
    return redirect("/")

@app.route('/download/<uuid>')
def download(uuid):
    return("INCOMPLETE")

@app.route("/delete/<uuid>")
def delete(uuid):
    rmtree(dutil.getDir(uuid))
    return redirect("/")

app.run(debug=True, host= HOST, port=PORT)