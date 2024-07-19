import sqlite3
import os

DB = sqlite3.connect("APKupcase.db",check_same_thread=False)
cursor = DB.cursor()



def Profile():
    Setprofile = '''
        CREATE TABLE Profile (
            id INT PRIMARY KEY,
            image VARCHAR(500),
            name VARCHAR(500),
            profession VARCHAR(500),
            company VARCHAR(500),
            status VARCHAR(500),
            birth DATETIME
            
        )
    '''
    return Setprofile

def Note():
    setNote = '''
        CREATE TABLE note (
            title VARCHAR(900) PRIMARY KEY,
            textiled TEXT
        )
    '''
    return setNote
def Item():
    setItem = '''
        CREATE TABLE item (
            name VARCHAR(500) PRIMARY KEY
        )
    '''
    return setItem
def List():
    SetList = '''
        SELECT * FROM Profile
    '''
    return SetList

def Drop():
    dropCmd = '''ALTER TABLE profile DROP COLUMN note'''
    return dropCmd

def PragmaList():
    Pragma = '''PRAGMA table_list'''
    return Pragma
try:
    Insert_DB_query = f'''
            INSERT INTO Profile (id,name,profession,company,status,birth)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
    tub = [1,'None','None','None','Offline','dd/mm/yy']
    if sqlite3.Connection:
        print("Connection set up")
        cursor.execute(Insert_DB_query,tub)
        # print("Release list of table")
        # for obj in cursor.fetchall():
        #     print(obj[0])
        # print("Command in process")
        DB.commit()
    elif sqlite3.Error:
        print("DB Error")
except sqlite3.Error as error:
    print(error)
         



