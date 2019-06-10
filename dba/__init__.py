#!/usr/bin/env python
# -*- coding: utf-8 -*-
    
from dba.chat import save_chat
from dba.chat import load_all_chats
from dba.core import DBA

def connect(name):
    if connect.singleton is None:
        connect.singleton = DBA(name)
    return connect.singleton


connect.singleton = None

