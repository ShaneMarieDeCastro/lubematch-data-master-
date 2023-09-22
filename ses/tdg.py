import json
import requests
import pandas as pd
import sqlite3


def tdg_table(api_key, sqlite):
    r = requests.get(
        'https://shell-livedocs.com/home/api', verify=False, params={'apiKey': api_key})
    sar = r.json()

    with open('tdg_data.json', 'w', encoding='utf8') as f:
        json.dump(sar, f)

    s = open('tdg_data.json', encoding='utf8')
    sar = json.load(s)

    phys_char = list()
    descriptions = list()
    short_marketing = list()

    for o in sar:
        for tpt in o['typicalPhysicalTable']:
            language = tpt['languageCode']
            for t in tpt['typicalPhysicalRow']:
                # for t in o['typicalPhysicalRow']:
                for r in t['typicalPhysicalColumn']:
                    phys_char.append((o['saleableProductCode'], o['saleableProductName'], t['property'],
                                      t['method'], t['unitOfMeasurement'], t['units'], r['name'], r['value'], language))

        for e in o['productDescriptor']:
            if e['title'] is None:
                continue
            if e['title'] == '':
                continue
            descriptions.append((o['saleableProductCode'],
                                 o['saleableProductName'], e['language'], e['title']))

        for e in o['shortMarketingText']:
            short_marketing.append(
                (o['saleableProductCode'], o['saleableProductName'], e['language'], e['body']))

    conn = sqlite3.connect(sqlite)

    headers_phys_char = ['GLOBALPRODUCTCODE', 'EXTERNALNAME', 'PROPERTY',
                         'METHOD', 'UNITOFMEASURE', 'UNITS', 'NAME', 'VALUE', 'LANGUAGE']
    df = pd.DataFrame(columns=headers_phys_char)
    for row in phys_char:
        df = df.append({
            'GLOBALPRODUCTCODE': row[0],
            'EXTERNALNAME': row[1],
            'PROPERTY': row[2],
            'METHOD': row[3],
            'UNITOFMEASURE': row[4],
            'UNITS': row[5],
            'NAME': row[6],
            'VALUE': row[7],
            'LANGUAGE': row[8]
        }, ignore_index=True)
    df.to_sql('TDG_PHYS_CHAR', conn, if_exists='replace', index=False)

    headers = ['GLOBALPRODUCTCODE', 'EXTERNALNAME', 'LANGUAGE', 'TEXT']
    df = pd.DataFrame(columns=headers)
    for row in short_marketing:
        df = df.append({
            'GLOBALPRODUCTCODE': row[0],
            'EXTERNALNAME': row[1],
            'LANGUAGE': row[2],
            'TEXT': row[3]
        }, ignore_index=True)
    df.to_sql('TDG_MARKETING_TEXT', conn, if_exists='replace', index=False)

    headers = ['GLOBALPRODUCTCODE', 'EXTERNALNAME', 'LANGUAGE', 'TEXT']
    df = pd.DataFrame(columns=headers)
    for row in descriptions:
        df = df.append({
            'GLOBALPRODUCTCODE': row[0],
            'EXTERNALNAME': row[1],
            'LANGUAGE': row[2],
            'TEXT': row[3]
        }, ignore_index=True)
    df.to_sql('TDG_DESCRIPTIONS', conn, if_exists='replace', index=False)

    conn.close()
