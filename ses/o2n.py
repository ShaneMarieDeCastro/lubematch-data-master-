import pandas as pd
import sqlite3
from collections import defaultdict


def o2n_table(path, sqlite):
    df = pd.read_excel(path)
    conn = sqlite3.connect(sqlite)
    df.to_sql('OLD2NEW', conn, if_exists='replace', index=False)
    conn.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def o2n_products(sqlite):
    conn = sqlite3.connect(sqlite)
    conn.row_factory = dict_factory
    c = conn.cursor()
    query = "SELECT DISTINCT * FROM OLD2NEW AS O2N"

    rows = defaultdict(list)
    for row in c.execute(query):
        key = "{} {} {} {}".format(row['companyName'],
                                   row['productName'],
                                   row['countryCode'],
                                   row['locale'])
        rows[key].append(row)
    l = []

    for k, v in rows.items():
        product = {
            "company": v[0]['companyName'],
            "name": v[0]['productName'],
            "countryCode": v[0]['countryCode'],
            "locale": v[0]['locale'],
            "alternatives": []}
        l.append(product)

        alternatives = [
            alternative for alternative in v if alternative['suitability'] < 3]

        for alternative in alternatives:
            product['alternatives'].append({
                "id": alternative['currentShellProductCode'],
                "name": alternative['currentShellProduct'],
                "competitorComments": alternative['competitorProductComments'],
                "suitability": alternative['suitability'],
            })
    return l
