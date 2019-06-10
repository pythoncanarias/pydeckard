#!/usr/bin/env python


from .core import DBA


# Highlevel functions



def save_chat(db, id_chat, chat_type, title):
    exists = db.get_row('SELECT * FROM chat where id_chat=?', id_chat)
    if not exists:
        sql = 'INSERT INTO chat (id_chat, chat_type, title) VALUES (?, ?, ?)'
        db.execute(sql, (id_chat, chat_type, title))
        return 1


def load_all_chats(db):
    return db.get_rows('SELECT * FROM chat')
