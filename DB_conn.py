from typing import Any

from pymysql import cursors, connect, IntegrityError
from tokens import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


def execute(sql: str, params: tuple = (), fetchone=False, fetchall=False):
    database_connection = connect(
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        cursorclass=cursors.DictCursor
    )

    cursor = database_connection.cursor()
    cursor.execute(sql, params)

    data = None

    if fetchone:
        data = cursor.fetchone()
    elif fetchall:
        data = cursor.fetchall()

    database_connection.commit()
    database_connection.close()

    return data


def register_user(telegram_id: str, fullname: str) -> None:
    sql = "INSERT INTO users (telegram_id, fullname) VALUES (%s, %s)"
    execute(sql, (telegram_id, fullname))


def get_user(telegram_id: int) -> dict | None:
    sql = "SELECT * FROM users WHERE telegram_id = %s"
    user = execute(sql, (telegram_id,), fetchone=True)
    return user


def register_city(telegram_id: int, city_name: str):
    user = get_user(telegram_id)
    if user:
        user_id = user["id"]
        try:
            sql = "INSERT INTO cities (`user`, name) VALUES (%s, %s)"
            execute(sql, (user_id, city_name))
        except IntegrityError:
            pass


def get_user_cities(telegram_id: int) -> list[Any]:
    user = get_user(telegram_id)
    if not user:
        return []
    user_id = user["id"]
    sql = "SELECT name FROM cities WHERE `user` = %s"
    cities = execute(sql, (user_id,), fetchall=True)
    if not cities:
        return []
    return [city["name"] for city in cities]

def check_if_user_id_available(telegram_id: int) -> bool:
    user = telegram_id
    sql = "SELECT id FROM users WHERE telegram_id = %s"
    user = execute(sql, (user,), fetchone=True)
    if user:
        return True
    else:
        return False

def delete_from_user_cities(telegram_id: int) -> None:
    user = get_user(telegram_id)
    try:
        sql = "DELETE FROM cities WHERE `user` = %s"
        execute(sql, (user["id"],))
    except IntegrityError:
        ...
