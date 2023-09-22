import pandas as pd
import sqlite3


def packshot_table(path, sqlite):
    df = pd.read_excel(path)
    conn = sqlite3.connect(sqlite)
    df.to_sql('PACKSHOTS', conn, if_exists='replace',
              index=False, dtype='text')
    conn.close()
