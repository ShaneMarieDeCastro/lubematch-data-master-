import sqlite3
import cx_Oracle
import pandas as pd

cx_Oracle.init_oracle_client(lib_dir=r"C:\Oracle\InstantClient_x64\12.2.0")

class GPC():
    def __init__(self, connection_string, sqlite):
        self.oracle_connection = cx_Oracle.connect(
            connection_string, encoding="UTF-8")
        self.sqlite_connection = sqlite3.connect(sqlite)

        self.tables = [
            ("RBV.LUBCHT_SALEABLEPRODUCT", "SALEABLEPRODUCT"),
            ("RBV.LUBCHT_PROD_SKU_COUNTRY", "PROD_SKU_COUNTRY"),
            ("RBV.LUBCHT_SALEPRODCOUNTRY", "SALEPRODCOUNTRY"),
            ("RBV.LUBCHT_SP_COUNTRY_DOC", "SP_COUNTRY_DOC"),
            ("RBV.LUBCHT_PRODUCT_SKU", "PRODUCT_SKU"),
            ("RBV.LUBCHT_DOCUMENT", "DOCUMENT"),
            ("RBV.LUBCHT_PROD_NAME_HIER", "PROD_NAME_HIER"),
            ("RBV.LUBCHT_PACK", "PACK"),
            ("RBV.LUBCHT_SKU_VARIANT", "SKU_VARIANT"),
            ("RBV.LUBCHT_PROD_CLASSFTN", "PROD_CLASSFTN"),
            ("RBV.LUBCHT_GRADE_HIER", "GRADE_HIER"),
            ("RBV.LUBCHT_COUNTRY", "COUNTRY"),
            ("RBV.LUBCHT_LANGUAGE", "LANGUAGE"),
            ("RBV.LUBCHT_STAT_HIER", "STAT_HIER"),
            ("RBV.LUBCHT_PROD_MARKET_HIER", "PROD_MARKET_HIER"),
            # ("RBV.LUBCHT_DOCUMENTFORMAT", "DOCUMENTFORMAT"),
            ("RBV.LUBCHT_SP_MAT_STANDARD", "SPECS_PRODUCT"),
            ("RBV.LUBCHT_MATERIAL_STANDARD", "SPECS_LOOKUP"),
            ("RBV.LUBCHT_PACK_SIZE", "PACK_SIZE"),
            ("RBV.LUBCHT_PACK_UOM", "PACK_UOM"),
            ("RBV.LUBCHT_BASE_FLUID_GROUP", "BASE_FLUID"),
            ("RBV.LUBCHT_BASE_FLUID_SUB_GROUP", "BASE_FLUID_SUB"),
            ("RBV.LUBCHT_ORGANISATION", "ORGANISATION"),
        ]

    def clone_all(self):
        for table in self.tables:
            self.clone(table[0], table[1])

    def clone(self, table_name, desired_name):
        query = '''
        SELECT * FROM {}
        '''.format(table_name)
        df = pd.read_sql(query, self.oracle_connection)
        df.to_sql(desired_name, self.sqlite_connection,
                  if_exists='replace', index=False)

    def close(self):
        self.sqlite_connection.close()
        self.oracle_connection.close()


def gpc_tables(connection, sqlite):
    try:
        gpc = GPC(connection, sqlite)
        gpc.clone_all()
        gpc.close()
    except Exception as e:
        print(e)
