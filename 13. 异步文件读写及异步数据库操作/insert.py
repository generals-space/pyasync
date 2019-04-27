import time

import psycopg2

db_config = {
    'host': 'localhost',
    'port': '5432',
    'database': 'mydb',
    'user': 'my',
    'password': '123456',
}

db_conn = psycopg2.connect(**db_config)

def initdb():
    cursor = db_conn.cursor()
    cursor.execute('create table if not exists test(id serial primary key, name varchar(50));')
    cursor.execute('delete from test;')
    db_conn.commit()
    cursor.close()

def insert(i):
    name = 'name-{:d}'.format(i)
    cursor = db_conn.cursor()
    cursor.execute('insert into test(name) values(%s);', (name,))
    db_conn.commit()
    cursor.close()

initdb()

start = time.time()
for i in range(10000): insert(i)
end = time.time()
db_conn.close()

print('cost %f' % (end - start))
