import sqlite3

def get_connection():

    conn = sqlite3.connect('roads_of_russia.sqlite')

    return conn
