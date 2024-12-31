
import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',       
        password= "39039",
        database='multifunctional_citizen_app',
        port= 3306,
        cursorclass=pymysql.cursors.DictCursor
    )
def get_users():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user;")
            users = cursor.fetchall()
        print(users)
    except Exception as e:
        return {'error': str(e)}
    finally:
        connection.close()

get_users()