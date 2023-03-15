import os
import json
# from app import datapath

datapath = 'app/data'

def loadData():
    fileNamesList = []
    descriptionList = []
    uploadDateList = []
    uuidList = []
    dirlist = os.listdir(datapath)
    for i in dirlist:
        if os.path.isdir(os.path.join(datapath, i)):
            with open(os.path.join(datapath, i, 'data.json'), 'r') as f:
                infojson = json.load(f)
            fileNamesList.insert(0, infojson['file_name'])
            descriptionList.insert(0, infojson['description'])
            uploadDateList.insert(0, infojson['date_uploaded'])
            uuidList.insert(0, infojson['uuid'])
    return fileNamesList, descriptionList, uploadDateList, uuidList

def getDir(uuid):
    thedir = ""
    if os.path.isdir(os.path.join(datapath, uuid)):
        with open(os.path.join(datapath, uuid, 'data.json'), 'r') as f:
            infojson = json.load(f)
        if uuid == infojson['uuid']:
            thedir = os.path.join(datapath, uuid)
    return(thedir)

def updateDesc(uuid, text):
    if os.path.isdir(os.path.join(datapath, uuid)):
        with open(os.path.join(datapath, uuid, 'data.json'), 'r') as f:
            infojson = json.load(f)
        if uuid == infojson['uuid']:
            infojson['description'] = text
            with open(os.path.join(datapath, uuid, "data.json"), 'w') as f:
                json.dump(infojson, f)

def getFile(uuid):
    filename = ""
    if os.path.isdir(os.path.join(datapath, uuid)):
        with open(os.path.join(datapath, uuid, 'data.json'), 'r') as f:
            infojson = json.load(f)
        if uuid == infojson['uuid']:
            filename = infojson['file_name']
    return(filename)
