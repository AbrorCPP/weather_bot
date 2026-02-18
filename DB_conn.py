from pymysql import cursors,connect,IntegrityError
from tokens import DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME

def execute(sql: str, params: tuple=(), fetchone=False):
    database_connection = connect(
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        cursorclass=cursors.DictCursor
    )
    cursor = database_connection.cursor()
    cursor.execute(sql,params)
    data = None
    if fetchone:
        data = cursor.fetchone()


    database_connection.commit()
    database_connection.close()

    return data

def register_user(telegram_id: str, fullname: str) -> None:
    sql = "INSERT INTO users (telegram_id, fullname) VALUES (%s, %s)"
    execute(sql, (telegram_id, fullname))

def get_user(telegram_id: str) -> dict|None:
    sql = "SELECT * FROM users WHERE telegram_id = %s"
    user = execute(sql, (telegram_id,), fetchone=True)
    return user

def register_city(telegram_id: str, city_name: str):
    user = get_user(telegram_id)
    if user:
        user_id = user.get("id")
        try:
            sql = "INSERT INTO cities (user, name) VALUES (%s, %s)"
            execute(sql, (user_id, city_name))
        except IntegrityError:
            ...

