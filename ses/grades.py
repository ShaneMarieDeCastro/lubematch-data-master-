import pandas as pd
import sqlite3


def grade_names_table(path, sqlite):
    df = pd.read_excel(path)
    conn = sqlite3.connect(sqlite)
    df.to_sql('GRADE_NAME', conn, if_exists='replace',
              index=False, dtype='text')
    conn.close()
