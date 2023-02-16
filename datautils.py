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
    dirlist = os.listdir('data')
    for i in dirlist:
        if os.path.isdir("data/" + i):
            with open(os.path.join('data', i, 'data.json'), 'r') as f:
                infojson = json.load(f)
            if uuid == infojson['uuid']:
                global thedir
                thedir = os.path.join('data', i)
                break
    return(thedir)            