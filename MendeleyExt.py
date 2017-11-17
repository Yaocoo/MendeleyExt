#!/usr/bin/python

import os
import sys
import sqlite3
import configparser

# define variables.
##
cfgFile = 'config.cfg'

# parse configurations
##
if os.path.exists(os.path.join(os.getcwd(), cfgFile)):
    cfg = configparser.ConfigParser()
    cfg.read('config.cfg')
    dbName = cfg.get('Global', 'dbName')
    localFilePath = cfg.get('Global', 'localFilePath')
    parentFolder = cfg.get('Global', 'parentFolder')
else:
    try:
        sys.exit(1)
    except:
        print('config file missing!')

# 
##
parentFolder = '/' + parentFolder + '/'
localFilePath = 'file:///' + localFilePath

# Database process
##
if os.path.exists(dbName):
    conn = sqlite3.connect(dbName)  # connect to database
    cursor = conn.cursor()
    cursor.execute('SELECT localUrl FROM Files;')
    localURL = cursor.fetchall()
    for st in localURL:
        oldUrl = st[0]
        if oldUrl.find(parentFolder) != -1:
            sParts = oldUrl.split(parentFolder)
            newUrl = oldUrl.replace(sParts[0],localFilePath)
            cursor.execute('UPDATE Files SET localUrl = ? WHERE localUrl = ?;', (newUrl, oldUrl))
    # Close cursor
    cursor.close()
    # Commit transaction
    conn.commit()
    # Close connection
    conn.close()

else:
    try:
        sys.exit(1)
    except:
        print('Invalid database file!')
