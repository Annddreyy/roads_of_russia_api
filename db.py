import sqlite3

import pyodbc

def get_connection():

    conn = sqlite3.connect('roads_of_russia.sqlite')

    return conn
