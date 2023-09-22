from encodings import utf_8
from numpy import short
import pandas as pd
import json
import requests
api_key = 'FB5C83957847A6D6862807A86EACF9AA'
r = requests.get(
    'https://shell-livedocs.com/home/api', verify=False, params={'apiKey': api_key})
sar = r.json()
with open('tdg_data.json', 'w', encoding='utf8') as f:
    json.dump(sar, f)
# s = open('tdg_data.json', encoding='utf8')
sar = json.load(open('tdg_data.json', encoding='utf8'))
# print(sar[1])
phys_char = list()
descriptions = list()
short_marketing = list()
long_marketing = list()
# # ///////////////long marketing////////////////
for o in sar:
    for tpt in o['typicalPhysicalTable']:
        language = tpt['languageCode']
        for t in tpt['typicalPhysicalRow']:
            # for t in o['typicalPhysicalRow']:
            for r in t['typicalPhysicalColumn']:
                phys_char.append((o['saleableProductCode'], o['saleableProductName'], t['property'],
                                  t['method'], t['unitOfMeasurement'], t['units'], r['name'], r['value'], language))
for o in sar:
    for e in o['longMarketingText']:
        long_marketing.append(
            (o['saleableProductCode'], o['saleableProductName'], e['language'], e['body']))
    for e in o['productDescriptor']:
        if e['title'] is None:
            continue
        if e['title'] == '':
            continue
        descriptions.append(
            (o['saleableProductCode'], o['saleableProductName'], e['language'], e['title']))
    for e in o['shortMarketingText']:
        short_marketing.append(
            (o['saleableProductCode'], o['saleableProductName'], e['language'], e['body']))
        print(short_marketing)
headers = ['GLOBALPRODUCTCODE', 'EXTERNALNAME', 'LANGUAGE', 'TEXT']
long = pd.DataFrame(columns=headers)
for row in long_marketing:
    long = long.append({
        'source': 'long_marketing',
        'GLOBALPRODUCTCODE': row[0],
        'EXTERNALNAME': row[1],
        'LANGUAGE': row[2],
        'TEXT': row[3]
    }, ignore_index=True)
short = pd.DataFrame(columns=headers)
for row in short_marketing:
    short = short.append({
        'source': 'short_marketing',
        'GLOBALPRODUCTCODE': row[0],
        'EXTERNALNAME': row[1],
        'LANGUAGE': row[2],
        'TEXT': row[3]
    }, ignore_index=True)
desc = pd.DataFrame(columns=headers)
for row in descriptions:
    desc = desc.append({
        'source': 'descriptor',
        'GLOBALPRODUCTCODE': row[0],
        'EXTERNALNAME': row[1],
        'LANGUAGE': row[2],
        'TEXT': row[3]
    }, ignore_index=True)
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
df.to_csv('phys_char.csv', encoding='utf8')
all = [long, short, desc]
combine = pd.concat(all)
combine.to_csv('all_marketing.csv', encoding='utf8')
# df.to_csv('long_marketing.csv', encoding='utf8')
# df['TEXT'].fillna(0)
# df[df['TEXT'].str.contains('readily biodegradable')]
# print([df['GLOBALPRODUCTCODE']])
# /////////physical characteristics:////////////
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
        print(short_marketing)
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
df.to_csv('phys_char_text.csv', encoding='utf8')
# # ///////////short marketing//////////////
headers = ['GLOBALPRODUCTCODE', 'EXTERNALNAME', 'LANGUAGE', 'TEXT']
df = pd.DataFrame(columns=headers)
for row in short_marketing:
    df = df.append({
        'GLOBALPRODUCTCODE': row[0],
        'EXTERNALNAME': row[1],
        'LANGUAGE': row[2],
        'TEXT': row[3]
    }, ignore_index=True)
df.to_csv('short_marketing.csv', encoding='utf8')
# # /////////////product descriptor//////////////
headers = ['GLOBALPRODUCTCODE', 'EXTERNALNAME', 'LANGUAGE', 'TEXT']
df = pd.DataFrame(columns=headers)
for row in descriptions:
    df = df.append({
        'GLOBALPRODUCTCODE': row[0],
        'EXTERNALNAME': row[1],
        'LANGUAGE': row[2],
        'TEXT': row[3]
    }, ignore_index=True)
df.to_csv('descriptor.csv', encoding='utf8')