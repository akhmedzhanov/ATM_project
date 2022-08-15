
from config import host, user, password, db_name
import pymysql


#just create db on your localhost with name 'atm_db'

def connect_db():
    #create connection to 'atm_db' on localhost
    connection = None
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            cursorclass = pymysql.cursors.DictCursor
            )
    except Exception as ex:
        print("Connection refused!")
        print(ex)
       
    return connection


def create_table(connection, create_table_query):
    #create table
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.close()
    except Exception as ex:
        print(ex)
      
        
def insert_data(connection, insert_query):
    #insert data
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query)
        connection.commit()
    except Exception as ex:
        print(ex)

def select_atm_to_fix(connection, select_query):
    #select info to choose offline ATM's
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute(select_query)
        results = cursor.fetchall()
        print("First of all, we need to fix these ATM's: \n")
        for result in results:
            print(f"Coordinates: {result['coordinates']}, with ID = {result['id']}") 
    
    except Exception as ex:
        print(ex)


def select_atm_to_withdraw(connection, select_query):
    #select info to choose ATM's with too much cash in cash slots (all slots have the same size)
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute(select_query)
        results = cursor.fetchall()
        print("\nAfter this, we should withdraw next ATM's: \n")
        for result in results:
            print(f"Coordinates: {result['coordinates']}, with ID = {result['id']}") 
    
    except Exception as ex:
        print(ex)

        
def select_atm_to_fill(connection, select_query):
    #select info to choose ATM's with not enough cash in cash slots
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute(select_query)
        results = cursor.fetchall()
        print("\nAnd only then we will fill those next ATM's:\n")
        for result in results:
            print(f"Coordinates: {result['coordinates']}, with ID = {result['id']}") 
    
    except Exception as ex:
        print(ex)