import sqlite3

def initializeDB():
    connection=sqlite3.connect('Project1\\firstProj\\database.db')
    with open('Project1\\firstProj\\schema.sql') as f:
        connection.executescript(f.read())