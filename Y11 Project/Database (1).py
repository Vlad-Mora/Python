import datetime
import time
from tkinter import *
import sqlite3

def createConnection():
    global database
    global connection
    fileName = "Database.db"
    try:
        connection = sqlite3.connect(fileName)
        database = connection.cursor()
    except Error as e:
        print(e)

def createTable(**kwargs):
    createConnection()
    
    query = f'CREATE TABLE IF NOT EXISTS {kwargs["tableName"]}('
    for column in kwargs["column"]:
        columnProps = " ".join(kwargs["column"][column]) + ", "
        columnQuery = f"{column} {columnProps}"
        query += columnQuery
    query = query[:len(query) - 2] + ');'

    print(f"Table '{kwargs['tableName']}' created.")
    
    try:
        database.execute(query)
    except Error as e:
        print(e)
        
    connection.commit()
    database.close()

def getTableContent(**kwargs):
    createConnection()
    
    orderByColumn = list(kwargs["sortBy"].keys())[0]
    orderByDirection = list(kwargs["sortBy"].values())[0]
    selectedColumns = ", ".join(kwargs["columns"])

    if kwargs["selectionStatement"] != "":
        query = f'SELECT {selectedColumns} FROM {kwargs["tableName"]} WHERE {kwargs["selectionStatement"]} ORDER BY {orderByColumn} {orderByDirection};'
    else:
        query = f'SELECT {selectedColumns} FROM {kwargs["tableName"]} ORDER BY {orderByColumn} {orderByDirection};'
        
    try:
        result = database.execute(query)
    except Error as e:
        print(e)
        
    connection.commit()
    database.close()
    
    return result.fetchall()

def writeTableContent(**kwargs):
    createConnection()
    
    columns = ', '.join(list(kwargs["data"].keys()))
    values = list(kwargs["data"].values())
    query = f"INSERT INTO {kwargs['tableName']} ({columns}) VALUES({values});"
    query = query.replace("[", "").replace("]", "")
   
    try:
        database.execute(query)
    except Error as e:
        print(e)
        
    connection.commit()
    database.close()
