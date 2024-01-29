import sqlite3

def checkLogin(email):
    connection=sqlite3.connect('Project1\\firstProj\\database.db')
    cur=connection.cursor()
    cmd="SELECT EMAIL, PASSWRD FROM USERS WHERE EMAIL=(?)"
    cur.execute(cmd, (email,))

    user=cur.fetchone()
    print(user)
    connection.close()

    return user

# checkLogin('dummy@gmail.com')