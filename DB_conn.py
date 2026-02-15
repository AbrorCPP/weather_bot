from pymysql import cursors,connect
from tokens import DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME

def register_user(telegram_id,fullname):
    database_connection = connect(
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        cursorclass=cursors.DictCursor
    )
    cursor = database_connection.cursor()
    sql = f"""INSERT INTO users(telegram_id,fullname) VALUES(%s,%s)"""
    cursor.execute(sql,(str(telegram_id),fullname))
    database_connection.commit()
    database_connection.close()
