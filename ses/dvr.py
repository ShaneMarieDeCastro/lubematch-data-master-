import pandas as pd
import sqlite3


def dvr_table(path, sqlite):
    df = pd.read_excel(path)
    conn = sqlite3.connect(sqlite)
    df.to_sql('DVR', conn, if_exists='replace', index=False)
    conn.close()
