import sqlite3

def insert_question(email, ques, desc):
    connection=sqlite3.connect('Project1\\firstProj\\database.db')
    cur=connection.cursor()
    cmd="INSERT INTO QUESTION (EMAIL, QUESTION, DESCRIP) VALUES (?, ?, ?)"
    var=cur.execute(cmd, (email, ques, desc))

    print(var)

    connection.commit()
    connection.close()
    return var.lastrowid