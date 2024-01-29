import sqlite3

def addUser(user):
    connection=sqlite3.connect('Project1\\firstProj\\database.db')
    cur=connection.cursor()
    cmd="INSERT INTO USERS (EMAIL, PHN_NO, PASSWRD) VALUES (?, ?, ?)"
    var=cur.execute(cmd, user)

    print(var)

    connection.commit()
    connection.close()
    return var.lastrowid

def addImageUpload(row):
    connection=sqlite3.connect('Project1\\firstProj\\database.db')
    cur=connection.cursor()
    cmd="INSERT INTO UPLOADS (EMAIL, FILE_NAME, IMG_FILE, PREDICTION) VALUES (?, ?, ?, ?)"
    var=cur.execute(cmd, row)

    print(var)

    connection.commit()
    connection.close()
    return var.lastrowid