import sqlite3
import json


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def query(country):
    return '''
SELECT DISTINCT 
    sp.EXTERNALNAME
FROM SALEPRODCOUNTRY AS spc
LEFT JOIN SALEABLEPRODUCT AS sp ON spc.PRODUCT_ID=sp.PRODUCT_ID
LEFT JOIN STAT_HIER AS shsp ON shsp.STATUS_SUB_GROUP_ID=sp.STATUS_SUB_GROUP_ID 
LEFT JOIN STAT_HIER AS shspc ON shspc.STATUS_SUB_GROUP_ID=spc.STATUS_SUB_GROUP_ID
WHERE shsp.EXP_EPC='Y' AND shspc.EXP_EPC='Y' AND spc.COUNTRY_CODE='{}' 
    '''.format(country)


class Names():
    def __init__(self, path, country):
        self.path = path
        self.country = country
        self.conn = None
        self.__connect()

    def __connect(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = dict_factory

    def shell(self):
        c = self.conn.cursor()
        names = [row['EXTERNALNAME'] for row in c.execute(query(self.country))]
        print(json.dumps(names))
        c.close()

    def close(self):
        self.conn.close()
