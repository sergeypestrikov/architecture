import sqlite3

connection = sqlite3.connect('patterns.sqlite')
current = connection.cursor()
with open('create_data_base.sql', 'r') as f:
    text = f.read()

current.executescript(text)
current.close()
connection.close()