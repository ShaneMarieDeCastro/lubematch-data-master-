import pandas as pd
import sqlite3


def sub_group_i18n(path, sqlite):
    df = pd.read_excel(path)
    conn = sqlite3.connect(sqlite)
    df.to_sql('PRODUCT_SUB_GROUP', conn, if_exists='replace',
              index=False, dtype='text')
    conn.close()
