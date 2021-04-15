import sqlite3
from queries import QUERIES
def sql(method, query, *args):
    res = None
    try:
        conn = sqlite3.connect('telegram_task.sqlite')
        cursor = conn.cursor()
        cursor.execute(QUERIES[query].format(*args[0]))
        if method=='select_one':
            res = cursor.fetchone()
        if method=='select_all':
            res = cursor.fetchall()
        if method in ('insert', 'update', 'delete'):
            conn.commit()
            res = cursor.lastrowid
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return res

