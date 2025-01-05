import os
from dotenv import load_dotenv
import pymysql

load_dotenv()


def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("AWS_RDS_HOST"),
            user='admin',
            password=os.getenv("AWS_RDS_PASSWORD"),
            database='multifunctional_citizen',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=120
        )
        print("Database connection successful!")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
