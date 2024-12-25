import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',       
        password= os.getenv("DB_PASSWORD"),
        database='multifunctional_citizen',
        port= 3306,
        cursorclass=pymysql.cursors.DictCursor
    )
