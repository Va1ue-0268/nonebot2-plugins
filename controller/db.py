import sqlite3
import os
import time
path = path = get_driver().config.plugin_data + 'controller'
db = path + '/data.db'

CONTROLLER_TABLE = 'Controller'
COLOR_TABLE = 'Color'
IR_TABLE = 'IR'

CONTROLLER_DEFAULT = '''
CREATE TABLE if not exists Controller(
    id INTEGER NOT NULL,
    uuid char(40) NOT NULL,
    nickname char(40) NOT NULL,
    is_default INTEGER NOT NULL DEFAULT 0,
    location char(20) NOT NULL,
    state INTEGER NOT NULL DEFAULT 0,
    type char(20) NOT NULL,
    PRIMARY KEY(id,uuid)
);
'''

COLOR_DEFAULT = '''
CREATE TABLE if not exists Color(
    id INTEGER NOT NULL,
    state INTEGER NOT NULL DEFAULT 0,
    R INTEGER NOT NULL DEFAULT 0,
    G INTEGER NOT NULL DEFAULT 0,
    B INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY(id,uuid)
);
'''

IR_DEFAULT = '''
CREATE TABLE if not exists IR(
    location PRIMARY KEY char(40) NOT NULL,
    value json
);
'''

def create_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(CONTROLLER_DEFAULT)
    c.execute(COLOR_DEFAULT)
    c.execute(IR_DEFAULT)
    conn.commit()
    conn.close()

def execute(sql:str):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    res = c.execute(sql)
    data = []
    if res:
        for i in res:
            data.append(i)
    conn.commit()
    conn.close()
    return data

'''
INSERT
'''
def add_device(id:int, uuid:str ,location:str ,type:str ,nickname:str):
    sql = f'''INSERT INTO {CONTROLLER_TABLE} (id, uuid, location, type, nickname) 
    values ("{id}", {uuid}, "{location}", "{type}", "{nickname}");'''
    execute(sql)

def add_color(id:int, uuid:str):
    sql = f'''INSERT INTO {COLOR_TABLE} (id, uuid) 
    values ("{id}", {uuid});'''
    execute(sql)


'''
SELECT
'''
def count_device(id:int, type:str):
    return execute(f"SELECT count(*) FROM {CONTROLLER_TABLE} where id = {id} and type = {type}")

def select_all(TABLE:str):
    return execute(f"SELECT * FROM {TABLE}")

def select_one(id:int, uuid:str, TABLE:str):
    return execute(f'SELECT * FROM {TABLE} where id = {id} and uuid = {uuid}')

'''
UPDATE
'''
def update_state(id:int, uuid:str ,field: str, value, TABLE:str):
    execute(f'UPDATE {TABLE} set {field} = "{value}" WHERE mid = {id} and gid = {uuid}')

'''
DELETE
'''
def delete_focus(id, uuid, TABLE:str):
    execute(f'DELETE FROM {TABLE} WHERE mid = {id} and gid = {uuid}')

create_table()
