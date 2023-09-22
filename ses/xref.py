import pandas as pd
import sqlite3
from collections import defaultdict


def xref_table(path, sqlite):
    df = pd.read_excel(path, usecols=[
        'countryCode',
        'locale',
        'companyName',
        'productName',
        'currentShellProductCode',
        'currentShellComments',
        'currentShellProduct',
        'suitability',
        'competitorProductComments',
        'contactInfo',
    ], keep_default_na=False)
    conn = sqlite3.connect(sqlite)
    df.to_sql('XREF', conn, if_exists='replace', index=False)
    conn.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def xref_products(sqlite):
    conn = sqlite3.connect(sqlite)
    conn.row_factory = dict_factory
    c = conn.cursor()
    query = "SELECT DISTINCT * FROM XREF AS XR"

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
                "shellComments": alternative['currentShellComments'],
                "competitorComments": alternative['competitorProductComments'],
                "suitability": alternative['suitability'],
            })
    return l
