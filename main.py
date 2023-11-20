import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def select_table_from_query(sql_split, query_type):
    if query_type == 'insert':
        query_table = sql_split.index('into') + 1
    elif query_type == 'update':
        query_table = sql_split.index('update') + 1
    else:
        query_table = sql_split.index('from') + 1

    table_name = sql_split[query_table]
    sql = 'SELECT * FROM ' + table_name

    return sql


def execute(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)

        print('Запит: ' + sql)

        sql_split = sql.lower().split()

        if sql_split[0] == 'select':
            rows = cur.fetchall()
            for row in rows:
                print(row)
            print()

        elif sql_split[0] == 'insert':
            print('Запис додано')
            execute(conn, select_table_from_query(sql_split, sql_split[0]))

        elif sql_split[0] == 'update' or sql_split[0] == 'delete':
            conn.commit()
            print('Запис змінено / видалено')
            execute(conn, select_table_from_query(sql_split, sql_split[0]))

    except Error as e:
        print(e)


def main():
    database = r"adress_book.db"

    conn = create_connection(database)

    with conn:
        print("1. Вивести всі записи з таблиці expenses")
        execute(conn, "SELECT * FROM contacts")

        print("2. Зміна номеру телефона в контакта anton")
        execute(conn, "UPDATE contacts SET phone = 380991112233 WHERE id = 1")

        print("3. Видалення льоні з контактів")
        execute(conn, "DELETE FROM contacts WHERE id = 3")

        print("4. Додати новий запис про витрати")
        execute(conn, """
                INSERT INTO
                contacts (id, name, email, phone)
                VALUES (3, 'nazar', 'nazar@gmail.com', 380957472905);
            """)


if __name__ == '__main__':
    main()
