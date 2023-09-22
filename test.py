from sqlalchemy import create_engine, Table, Column, String, MetaData

engine = create_engine('oracle+cx_oracle://IFGPC_DATA_LAYER:MeJgIp7$KA#DW!W@MUNTSA-A-RESH148P.europe.shell.com:1648/RESH148P')
conn = engine.connect()
# meta = MetaData()
# meta.reflect(bind=engine, schema='RBV',views=True)
# src = meta.tables['RBV.lubcht_saleableproduct']

# sqlite_engine = create_engine('sqlite:///new.sqlite')
# src.create(sqlite_engine)
# results = conn.execute('SELECT owner, object_name, object_type FROM ALL_OBJECTS')
# for r in results:
#     print(r)

import pandas as pd
import cx_Oracle
import sqlite3

# conn = cx_Oracle.connect('IFGPC_DATA_LAYER','MeJgIp7$KA#DW!W','MUNTSA-A-RESH148P.europe.shell.com:1648/RESH148P')
# query = '''
# SELECT * FROM RBV.LUBCHT_SALEABLEPRODUCT
# '''

df = pd.read_sql_table('RBV.LUBCHT_SALEABLEPRODUCT', conn, schema='RBV')
print(df)

sqlite_conn = sqlite3.connect('new.sqlite')
df.to_sql('SALEABLEPRODUCT',sqlite_conn)
