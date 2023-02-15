import os
import json


def loadData():
    fileNamesList = []
    descriptionList = []
    uploadDateList = []
    dirlist = os.listdir('data')
    for i in dirlist:
        if os.path.isdir("data/" + i):
            with open(os.path.join('data', i, 'data.json'), 'r') as f:
                infojson = json.load(f)
            fileNamesList.append(infojson['file_name'])
            descriptionList.append(infojson['description'])                
            uploadDateList.append(infojson['date_uploaded'])

    return fileNamesList, descriptionList, uploadDateList
