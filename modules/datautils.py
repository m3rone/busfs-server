import os
import json
from shutil import rmtree
import sqlite3

# from app import datapath

datapath = 'app/data'

def connectToDB():
    conn = sqlite3.connect("app/files.db")
    cursor = conn.cursor()
    return conn, cursor

def loadData():
    conn, cursor = connectToDB()
    cursor.execute("SELECT * FROM files")
    filelist = cursor.fetchall()

    return filelist

def delDir(uuid):
    conn, cursor = connectToDB()
    if os.path.isdir(thedir := os.path.join(datapath, uuid)):
        rmtree(thedir)
        cursor.execute("DELETE FROM files WHERE uuid = :uuidin", {"uuidin" : uuid})
    conn.commit()

def updateDesc(uuid, text):
    conn, cursor = connectToDB()
    if os.path.isdir(os.path.join(datapath, uuid)):
        cursor.execute("""UPDATE files
                       SET description = :newdesc
                       WHERE uuid = :uuidin""", {"newdesc" : text, "uuidin" : uuid})
    conn.commit()

def getFile(uuid):
    conn, cursor = connectToDB()
    filename = ""
    if os.path.isdir(os.path.join(datapath, uuid)):
        filename = cursor.execute("SELECT filename FROM files WHERE uuid = :uuidin", {"uuidin" : uuid}).fetchone()
    return(filename[0])

def addFileToDB(file, desc, todayformat, randstr):
    conn, cursor = connectToDB()
    cursor.execute("""INSERT INTO files (filename, description, upload_date, uuid) 
                       VALUES (:file, :desc, :upload, :uuid);""", {"file" : file.filename, "desc" : desc, "upload" : todayformat, "uuid" : randstr})
    conn.commit()

# def jsonLoad(keys:list = ["id", "filename", "description", "upload_date", "uuid"], values:list = loadData()):
#     conn, cursor = connectToDB()
#     jsonload = cursor.execute(""" SELECT json_group_array(json_object(
#                                     'id', id,
#                                     'filename', filename,
#                                     'description', description,
#                                     'upload_date', upload_date,
#                                     'uuid', uuid
#                                 ) FROM files;
#                             """)

#     return jsonload
