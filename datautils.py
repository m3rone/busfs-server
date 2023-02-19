import os
import json

def loadData():
    fileNamesList = []
    descriptionList = []
    uploadDateList = []
    uuidList = []
    dirlist = os.listdir('data')
    for i in dirlist:
        if os.path.isdir("data/" + i):
            with open(os.path.join('data', i, 'data.json'), 'r') as f:
                infojson = json.load(f)
            fileNamesList.append(infojson['file_name'])
            descriptionList.append(infojson['description'])
            uploadDateList.append(infojson['date_uploaded'])
            uuidList.append(infojson['uuid'])

    return fileNamesList, descriptionList, uploadDateList, uuidList

def getDir(uuid):
    thedir = ""
    if os.path.isdir("data/" + uuid):
        with open(os.path.join('data', uuid, 'data.json'), 'r') as f:
            infojson = json.load(f)
        if uuid == infojson['uuid']:
            thedir = os.path.join('data', uuid)
    return(thedir)

def updateDesc(uuid, text):
    if os.path.isdir("data/" + uuid):
        with open(os.path.join('data', uuid, 'data.json'), 'r') as f:
            infojson = json.load(f)
        if uuid == infojson['uuid']:
            infojson['description'] = text
            with open(f'data/{uuid}/data.json', 'w') as f:
                json.dump(infojson, f)

def getFile(uuid):
    filename = ""
    if os.path.isdir("data/" + uuid):
        with open(os.path.join('data', uuid, 'data.json'), 'r') as f:
            infojson = json.load(f)
        if uuid == infojson['uuid']:
            filename = infojson['file_name']
    return(filename)
