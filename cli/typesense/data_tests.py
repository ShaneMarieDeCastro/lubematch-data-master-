import json
import sys
import logging
import requests
import os


XREF_FILE_NAME = "xref.json"
OLD2NEW_FILE_NAME = 'o2n.json'
SUPPORTED_LOCALES = ['en_PH', 'en_SG', 'id_ID', 'fr_CA', 'en_MY', 'ru_RU',
                     'zh_CN', 'de_DE', 'en_US', 'en_IN', 'en_CA', 'en_GB']  # , 'en_IE', 'en_AU'

ACTIVE_PRODUCTS_FILE_NAME = 'active.json'
PRODUCTS_DIR = os.path.join("..", "..", "out")
INDEX_TEST = {
    'locale_check': ['xref', 'old2new', 'products'],
    'alternatives_check': ['xref', 'old2new'],
    'num_products': ['xref', 'old2new', 'products']

}


def should_check(index_name, test_name):
    return index_name in INDEX_TEST[test_name]


def locale_check(locales):
    if (locale in SUPPORTED_LOCALES for locale in locales):
        logging.info('All supported locales seem to be present')
        return True
    errmsg = 'Some supported locales seem to be missing from the data - ' + \
        str([locale for locale in SUPPORTED_LOCALES if locale not in locales])
    logging.error(errmsg)
    return False


def alternatives_check(data):
    products_without_alternatives = list(filter(lambda product: product['alternatives'] == [
    ] or product['alternatives'] == None, data))
    if len(products_without_alternatives):

        logging.warning('There are ' + str(len(products_without_alternatives)) +
                        ' product(s) without alternatives, they will be filtered out while updating the data')
    else:
        logging.info('All products have alternatives!')
    return True


def num_products(data, locale):
    TYPESENSE_SERVER_URI = "https://nexus-typesense.theagilehub.net"

    INDEX_URI = os.path.join(TYPESENSE_SERVER_URI,
                             "collections", index_name, "documents")

    query_string = "q=*&filter_by=locale:"+locale.replace('_', '-')

    res = requests.get(os.path.join(INDEX_URI, 'search?'+query_string),
                       headers={"Content-Type": "application/json",
                                "X-TYPESENSE-API-KEY": TYPESENSE_API_KEY
                                },
                       )

    if(res.status_code == 200):
        data_in_locale = list(filter(lambda x: x['locale'] == locale, data))

        new_number_products = len(data_in_locale)

        old_number_products = int(res.json()['found'])

        if new_number_products == old_number_products:
            logging.warning(
                'The number of %s products in locale %s is the same - %d; maybe redundant?', index_name, locale, new_number_products)
        else:
            logging.info('The number of %s products in locale %s is different - update:%d, production:%d',
                         index_name, locale, new_number_products, old_number_products)
        return True


def write_product_data_to_file():
    products_data = []
    num_products = 0
    for subdir, dirs, files in os.walk(PRODUCTS_DIR):
        num_products += len(list(filter(lambda x: x.endswith('.json'), files)))
        locale = str(subdir)[str(subdir).rindex('/')+1:]
        for f in files:
            try:
                with open(os.path.join(subdir, f), ) as f:
                    data = json.load(f)
                    data['locale'] = locale
                    products_data.append(data)
            except Exception as E:
                pass
    with open(ACTIVE_PRODUCTS_FILE_NAME, 'w') as products_file:
        json.dump(products_data, products_file)

    assert num_products == len(
        products_data), 'Something went wrong with the number of products written to the temporary json file'


if __name__ == '__main__':
    index_name, TYPESENSE_API_KEY = sys.argv[1], sys.argv[2]
    logging.basicConfig(level=logging.INFO)
    data_file_name = None

    if index_name == 'xref':
        data_file_name = XREF_FILE_NAME
    elif index_name == 'old2new':
        data_file_name = OLD2NEW_FILE_NAME
    elif index_name == 'products':
        write_product_data_to_file()
        data_file_name = ACTIVE_PRODUCTS_FILE_NAME

    with open(data_file_name, ) as f:
        data = json.load(f)

        locales = list(set(map(lambda x: x['locale'], data)))
        logging.info('%s has data for the following locales - %s',
                     data_file_name, str(locales))

        if should_check(index_name, 'locale_check'):
            if not locale_check(locales):
                sys.exit(1)

        if should_check(index_name, 'alternatives_check'):
            if not alternatives_check(data):
                sys.exit(1)

        if should_check(index_name, 'num_products'):
            for locale in locales:
                if not num_products(data, locale):
                    sys.exit(1)

        sys.exit(0)
