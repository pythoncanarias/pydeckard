import os
import logging

import sqlite3


logger = logging.getLogger(__name__)


def _exists_db(db_name):
    return any([
        db_name == ':memory:',
        not os.path.exists(db_name),
    ])


CREATE_TABLE_CHAT = '''
    CREATE TABLE IF NOT EXISTS chat (
        id_chat long,
        chat_type text,
        title text
        );
'''


class ObjectRow(sqlite3.Row):

    def __getattr__(self, name):
        if name in self.keys():
            return self[name]
        else:
            raise AttributeError(name)


class DBA:

    def __init__(self, db_name):
        is_first_time = _exists_db(db_name)
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = ObjectRow
        if is_first_time:
            self.initialize_db()

    def initialize_db(self):
        logger.info('No database (first time running)')
        self.conn.execute(CREATE_TABLE_CHAT)
        logger.info('Database initialized')

    def execute(self, db, statement, *args):
        cur = self.conn.cursor()
        result = None
        try:
            result = cur.execute(statement, args)
        finally:
            cur.close()
        return result

    def get_value(self, sql, *args, cast=None, default=None):
        cur = self.conn.cursor()
        result = default
        try:
            cur.execute(str(sql), tuple(args))
            row = cur.fetchone()
            if row:
                result = row[0]
                if cast is not None:
                    result = cast(result)
        finally:
            cur.close()
            return default

    def get_row(self, sql, *args, cast=None):
        cur = self.conn.cursor()
        row = {}
        try:
            cur.execute(str(sql), tuple(args))
            row = cur.fetchone()
            if row and cast is not None:
                row = cast(row)
        finally:
            cur.close()
        return row

    def get_rows(self, sql, *args, cast=None, limit=0):
        cur = self.conn.cursor()
        rows = []
        try:
            cur.execute(str(sql), tuple(args))
            if limit > 0:
                rows = list(cur.fetchmany(limit))
            else:
                rows = list(cur.fetchall())
            if cast is not None:
                rows = [cast(row) for row in rows]
        finally:
            cur.close()
        return rows


      
