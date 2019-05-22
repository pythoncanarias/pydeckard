import os

import sqlite3
from collections import OrderedDict
from collections.abc import MutableMapping

import config


class ObjectRow(sqlite3.Row):

    def __getattr__(self, name):
        if name in self.keys():
            return self[name]
        else:
            raise AttributeError(name)


def get_value(conn, sql, *args, cast=None):
    cur = conn.cursor()
    try:
        cur.execute(str(sql), tuple(args))
        row = cur.fetchone()
        if row:
            result = row[0]
            if cast is not None:
                result = cast(result)
            return result
        else:
            return default
    finally:
        cur.close()


def get_row(conn, sql, *args, cast=None):
    cur = conn.cursor()
    try:
        cur.execute(str(sql), tuple(args))
        row = cur.fetchone()
        if not row:
            return {}
        if cast is not None:
            row = cast(row)
        return row
    finally:
        cur.close()


def get_rows(conn, sql, *args, cast=None, limit=0):
    cur = conn.cursor()
    rows = []
    try:
        cur.execute(str(sql), tuple(args))
        if limit > 0:
            rows = cur.fetchmany(limit)
        else:
            rows = cur.fetchall()
        if cast is not None:
            rows = [cast(row) for row in rows]
        return list(rows)
    finally:
        cur.close()


CREATE_TABLE_CHAT = '''
    CREATE TABLE IF NOT EXISTS chat (
        id_chat long,
        title text,
        chat_type text
        )
'''

def initialize_db(conn):
    execute(conn, CREATE_TABLE_CHAT)

_conn = None


def get_connection():
    global _conn
    if _conn is None:
        db_name = config.DB_NAME
        first_time = any([
            db_name == ':memory:',
            not os.path.exists(db_name),
            ])
        _conn = sqlite3.connect(db_name)
        _conn.row_factory = ObjectRow
        if first_time:
            initialize_db(_conn)
    return _conn


def execute(db, statement, *args):
    cur = db.cursor()
    try:
        cur.execute(statement, args)
    finally:
        cur.close()



def save_chat(id_chat, chat_type, title):
    conn = get_connection()
    exists = get_row(conn, 'SELECT * FROM chat where id_chat=?', id_chat)
    if not exists:
        sql = 'INSERT INTO chat (id_chat, chat_type, title) VALUES (?, ?, ?)'
        execute(conn, sql, id_chat, chat_type, title)
        return 1

