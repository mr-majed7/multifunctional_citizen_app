import os 
from dotenv import load_dotenv
import pymysql

load_dotenv()



def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',       
        password=os.getenv("12345"),
        database='multifunctional_citizen_app', 
        cursorclass=pymysql.cursors.DictCursor
    )
