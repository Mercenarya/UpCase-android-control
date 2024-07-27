import sqlite3
import os



current = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current,"androidupcase.db")
DB = sqlite3.connect("androidupcase.db",check_same_thread=False)
cursor = DB.cursor()

print(db_path)

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
def Schedule():
    setSchedule = '''
        CREATE TABLE schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task VARCHAR(500),
            datepick DATETIME,
            timepick TEXT
        )
    '''
    return setSchedule
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

    Insert_DB_query_2 = f'''
            INSERT INTO schedule (id,task,datepick,timepick)
            VALUES (?, ?, ?, ?)
        '''
    tub_2 = [1,'Go to School','Tuesday','7:00 AM']
    if sqlite3.Connection:
        print("Connection set up")
        # cursor.execute(Item())
        # cursor.execute(Profile())
        # cursor.execute(Note())
        # cursor.execute(Schedule())
        # cursor.execute(Insert_DB_query,tub)
        # cursor.execute(Insert_DB_query_2,tub_2)
        # print("Release list of table")
        # print("Command in process")
        # cursor.execute("DROP TABLE schedule")
        DB.commit()
    elif sqlite3.Error:
        print("DB Error")
except sqlite3.Error as error:
    print(error)
         



