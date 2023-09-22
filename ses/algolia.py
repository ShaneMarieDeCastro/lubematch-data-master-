from ses.products import ProductsPacksDocs
import sqlite3
import json
import os


def Products(sqlite, sub_groups, marketing, desc, phys, country):
    # Call the products generation code and pick what we need for algolia
    p = ProductsPacksDocs(sqlite, sub_groups, marketing, desc, phys, country)
    products = p.lube_products()
    items = []
    for k, v in products.items():
        item = {
            'objectID': k,
            'GLOBAL_PRODUCT_CODE': k,
            'GRADE_NAME': v['GRADE_NAME'],
            'GRADE_RANK': grade_rank(v['GRADE_NAME']),
            'PROD_FAMILY_NAME': v['PROD_FAMILY_NAME'],
            'EXTERNALNAME': v['EXTERNALNAME'],
            'PROD_GROUP_NAME': v['PROD_GROUP_NAME'],
            'PROD_SUB_GROUP_NAME': v['PROD_SUB_GROUP_NAME'],
            'PROD_MARKET_NAME': v['PROD_MARKET_NAME'],
            'PROD_MARKET_RANK': prod_market_rank(v['PROD_MARKET_NAME']),
            'COUNTRY_CODE': v['COUNTRY_CODE'],
            'ACTIVE_COUNTRY': v['ACTIVE_COUNTRY'],
            'COMPANY': 'Shell',
        }
        items.append(item)
    print(json.dumps(items))


def ProductsIndex(directory):
    products = {}
    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(directory, filename)) as f:
            code = os.path.splitext(filename)[0]
            products[code] = json.load(f)

    items = []
    for k, v in products.items():
        item = {
            'objectID': k,
            'GLOBAL_PRODUCT_CODE': k,
            'GRADE_NAME': v['GRADE_NAME'],
            'GRADE_RANK': grade_rank(v['GRADE_NAME']),
            'PROD_FAMILY_NAME': v['PROD_FAMILY_NAME'],
            'EXTERNALNAME': v['EXTERNALNAME'],
            'PROD_SUB_GROUP_NAME': v['PROD_SUB_GROUP_NAME'],
            'PROD_MARKET_NAME': v['PROD_MARKET_NAME'],
            'PROD_MARKET_RANK': prod_market_rank(v['PROD_MARKET_NAME']),
            'COUNTRY_CODE': v['COUNTRY_CODE'],
            'ACTIVE_COUNTRY': v['ACTIVE_COUNTRY'],
            'SPECS': [spec['SPECIFICATION'] for spec in v['SPECS']],
            'COMPANY': 'Shell',
        }
        items.append(item)
    print(json.dumps(items))


market_ranks = {
    'Top': 5,
    'Premium': 4,
    'Mainstream': 3,
    'OEM Speciality': 2,
    'Entry': 1,


}


def prod_market_rank(name):
    if name in market_ranks:
        return market_ranks[name]
    else:
        return 1


grade_ranks = {
    "0W": 100,
    "0W-16": 110,
    "0W-20": 120,
    "0W-30": 130,
    "0W-40": 140,
    "0W-50": 150,
    "5W": 200,
    "5W-20": 210,
    "5W-30": 220,
    "5W-40": 230,
    "5W-50": 240,
    "10W": 300,
    "10W-20": 310,
    "10W-30": 320,
    "10W-40": 330,
    "10W-50": 340,
    "10W-60": 350,
    "15W": 400,
    "15W-30": 410,
    "15W-40": 420,
    "15W-50": 430,
    "20W": 500,
    "20W-20": 510,
    "20W-30": 520,
    "20W-40": 530,
    "20W-50": 540,
    "20W-60": 560,
    "20": 610,
    "30": 620,
    "40": 630,
    "50": 640,
    "60": 650,
    "80": 660,
    "90": 670,
    "140": 680,
    "250": 690,
    "70W": 700,
    "70W-90": 710,
    "70W-140": 720,
    "75W": 800,
    "75W-80": 810,
    "75W-85": 820,
    "75W-140": 830,
    "75W-90": 830,
    "75W-110": 840,
    "80W": 900,
    "80W-90": 910,
    "80W-140": 920,
    "85W": 1000,
    "85W-90": 1010,
    "85W-140": 1020,
    "90W-140": 1110,
    "25W-50": 1210,
    "25W-60": 1220,
    "2": 1301,
    "3": 1302,
    "4": 1303,
    "5": 1304,
    "7": 1305,
    "8": 1306,
    "9": 1307,
    "10": 1308,
    "11": 1309,
    "12": 1310,
    "13": 1311,
    "14": 1312,
    "15": 1313,
    "16": 1314,
    "17": 1315,
    "18": 1316,
    "19": 1317,
    "22": 1319,
    "23": 1320,
    "25": 1321,
    "26": 1322,
    "27": 1323,
    "32": 1325,
    "33": 1326,
    "36": 1327,
    "37": 1328,
    "43": 1330,
    "44": 1331,
    "45": 1332,
    "46": 1333,
    "48": 1334,
    "49": 1335,
    "55": 1336,
    "56": 1337,
    "68": 1338,
    "75": 1339,
    "78": 1340,
    "84": 1342,
    "85": 1343,
    "96": 1344,
    "100": 1345,
    "110": 1346,
    "120": 1347,
    "121": 1348,
    "125": 1349,
    "150": 1351,
    "165": 1352,
    "180": 1353,
    "200": 1354,
    "214": 1355,
    "220": 1356,
    "270": 1357,
    "290": 1358,
    "320": 1359,
    "410": 1360,
    "460": 1361,
    "530": 1362,
    "570": 1363,
    "680": 1364,
    "800": 1365,
    "1000": 1366,
    "1500": 1367,
    "1600": 1368,
    "2200": 1369,
    "3000": 1370,
    "3200": 1371,
    "4000": 1372,
    "4600": 1373,
    "4800": 1374,
    "6500": 1375,
    "6800": 1376,
    "9000": 1377,
    "11000": 1378,
    "13500": 1379,
    "20000": 1380,
    "0": 1403,
    "0.5": 1404,
    "1": 1405,
    "1.5": 1406,
    "2.5": 1408,
    "6": 1412,
    "0/00": 1416,
    "00/000": 1417,
    "0.035": 1501,
    "240": 1510,
    "280": 1511,
    "380": 1513,
    "420": 1514,
}


def grade_rank(name):
    if name in grade_ranks:
        return grade_ranks[name]
    else:
        return 10000
