import pandas as pd
import sqlite3


def base_oil_sub_group_table(path, sqlite):
    df = pd.read_excel(path)
    conn = sqlite3.connect(sqlite)
    df.to_sql('BASE_OIL_SUB_GROUP', conn, if_exists='replace',
              index=False, dtype='text')
    conn.close()


def base_oil_group_table(path, sqlite):
    df = pd.read_excel(path)
    conn = sqlite3.connect(sqlite)
    df.to_sql('BASE_OIL_GROUP', conn, if_exists='replace',
              index=False, dtype='text')
    conn.close()
