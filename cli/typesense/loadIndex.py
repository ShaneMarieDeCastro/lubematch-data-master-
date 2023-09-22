import json
import requests
import sys
import os
import uuid
import threading
from tqdm import tqdm


TYPESENSE_SERVER_URIS = {
    "local": "http://localhost:8108/collections",
    "remote": "https://preprod.products-gql.theagilehub.net/collections"
}
TYPESENSE_API_KEYS = {
    "local": "duIpsVTnbWkmsVokzxhj",
    "remote": "duIpsVTnbWkmsVokzxhj"
}

XREF_FILE_NAME = "xref.json"
OLD2NEW_FILE_NAME = "o2n.json"
PRODUCTS_DIR = os.path.join("..", "..", "out")
PRODUCT_FAMILIES_FILE_NAME = "product_families.json"


XREF_INDEX = "xref"
OLD2NEW_INDEX = "old2new"
PRODUCTS_INDEX = "products"
PRODUCT_FAMILY_INDEX = "product-families"

POSITION_MAP = {
    "-": 5,
    "Mainstream": 8,
    "OEM Speciality": 6,
    "Premium": 9,
    "Do Not Use..Value": 5,
    "Top": 10,
    "Entry": 7
}

FIELD_MAP = {
    "xref": ["name", "countryCode", "locale", "company", "alternatives", "uuid"],
    "products": ["countryCode", "name", "description", "family", "category", "position", "viscosityGrade", "viscosityType", "fluidType", "globalDocs", "localDocs", "globalSpecs", "packs", "marketing", "physicalCharacteristics", "active", "uuid"],
    "old2new": ["name", "countryCode", "locale", "company", "alternatives"],
}


def generate_uuid():
    return 1


def handle_locale(locale):
    return locale.replace('_', '-')


def log_basic_info(instance, index_name):
    print("loading into", instance, "instance at:",
          TYPESENSE_SERVER_URIS[instance], "\ninto the index", index_name)


def field_check(data, index_name):
    return (list(data.keys()).sort() == FIELD_MAP[index_name].sort())


def add_material_codes(data):
    data["materialCodes"] = list(
        map(lambda x: x.get("materialCode", None), data["packs"]))
    data["materialCodes"] = list(
        filter(lambda x: x is not None, data["materialCodes"]))
    return data


def handle_xref_data(data):
    for line in tqdm(data):
        line["uuid"] = generate_uuid()
        line["locale"] = handle_locale(line["locale"])
        if field_check(line, index_name):
            push_to_index(instance, index_name, line)


def handle_old2new_data(data):
    for line in tqdm(data):
        line["uuid"] = generate_uuid()
        if field_check(line, index_name):
            push_to_index(instance, index_name, line)


def handle_product_families_data(data):
    for line in tqdm(data):
        line["uuid"] = generate_uuid()
        line["locale"] = line["Locale"]
        del(line["Locale"])
        line["description"] = line["Description"]
        del(line["Description"])
        line["image"] = line["Image"]
        del(line["Image"])
        push_to_index(instance, index_name, line)


def create_threads(no_of_threads, target_function, data):
    threads = []
    for i in range(no_of_threads):
        threads.append(threading.Thread(target=target_function, args=(
            data[(i*len(data))//no_of_threads:((i+1)*len(data))//no_of_threads],)))
    return threads


def delete_products_by_locale(index_name, locale):
    print("deleting products in locale:", locale)
    deletion_url = os.path.join(TYPESENSE_SERVER_URIS[instance],
                                index_name, "documents?filter_by=locale:"+locale)
    try:
        res = requests.delete(url=deletion_url,
                              headers={"Content-Type": "application/json",
                                       "X-TYPESENSE-API-KEY": TYPESENSE_API_KEYS[instance]
                                       }
                              )
        print(res.text)
        return res
    except Exception as e:
        print(e)


def create_index(instance, index_name):
    index_url = TYPESENSE_SERVER_URIS[instance]
    try:
        with open("schemas.json", "r") as schemas:
            schema = json.load(schemas)[index_name]

        res = requests.post(index_url,
                            headers={"Content-Type": "application/json",
                                     "X-TYPESENSE-API-KEY": TYPESENSE_API_KEYS[instance]
                                     },
                            data=json.dumps(schema)
                            )
        if res.status_code != 201:
            print(res.status_code, res.text)
        return True
    except Exception as E:
        print(E)
        return False


def create_synonyms(instance, index_name):
    synonym_url = os.path.join(
        TYPESENSE_SERVER_URIS[instance], index_name, "synonyms")
    try:
        with open("synonyms.json", "r") as synonyms:
            synonyms_list = json.load(synonyms)[index_name]

        for synonym in synonyms_list:
            res = requests.put(os.path.join(synonym_url, str(uuid.uuid4())),
                               headers={"Content-Type": "application/json",
                                        "X-TYPESENSE-API-KEY": TYPESENSE_API_KEYS[instance]
                                        },
                               data=json.dumps(synonym)
                               )
            if res.status_code != 201:
                print(res.status_code, res.text)
        return True
    except Exception as E:
        print(E)
        return False


def push_to_index(instance, index_name, data):
    index_url = os.path.join(
        TYPESENSE_SERVER_URIS[instance], index_name, "documents")
    try:
        res = requests.post(index_url,
                            headers={"Content-Type": "application/json",
                                     "X-TYPESENSE-API-KEY": TYPESENSE_API_KEYS[instance]
                                     },
                            data=json.dumps(data)
                            )
        if res.status_code != 201:
            print(res.status_code)
        return True
    except Exception as E:
        print(E)
        return False


if __name__ == '__main__':
    instance, index_name = (sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else print(
        "usage: python3 loadIndex.py <local/remote> <xref/products/old2new/all>")

    index_names = ["xref", "products", "old2new",
                   "product-families"] if index_name == "all" else [index_name]

    for index in index_names:
        create_index(instance, index)
        create_synonyms(instance, index)
        print("collection and synonyms created for index", index)

    if XREF_INDEX in index_names:
        index_name = XREF_INDEX
        log_basic_info(instance, index_name)
        try:
            with open(XREF_FILE_NAME, ) as f:
                data = json.load(f)

            threads = create_threads(4, handle_xref_data, data)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

        except Exception as E:
            print(E)

    if PRODUCTS_INDEX in index_names:
        index_name = PRODUCTS_INDEX
        log_basic_info(instance, index_name)
        print(PRODUCTS_DIR)
        for subdir, dirs, files in os.walk(PRODUCTS_DIR):
            print(subdir, len(files))
            locale = str(subdir)[str(subdir).rindex('/')+1:]
            delete_products_by_locale(index_name, locale)
            print("inserting products into the index")
            for f in tqdm(files):
                try:
                    with open(os.path.join(subdir, f), ) as f:
                        data = json.load(f)
                    data["locale"] = str(subdir)[str(subdir).rindex('/')+1:]
                    data["objectId"] = data["id"]
                    data.pop("id")
                    data["uuid"] = generate_uuid()
                    data["position_number"] = POSITION_MAP[data.get(
                        "position", 1)]
                    data = add_material_codes(data)
                    if field_check(data, index_name):
                        result = push_to_index(instance, index_name, data)
                except Exception as E:
                    print(E)

    if OLD2NEW_INDEX in index_names:
        index_name = OLD2NEW_INDEX
        log_basic_info(instance, index_name)
        try:
            with open(OLD2NEW_FILE_NAME, ) as f:
                data = json.load(f)
            threads = create_threads(4, handle_old2new_data, data)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

        except Exception as E:
            print(E)

    if PRODUCT_FAMILY_INDEX in index_names:
        index_name = PRODUCT_FAMILY_INDEX
        log_basic_info(instance, index_name)
        try:
            with open(PRODUCT_FAMILIES_FILE_NAME, ) as f:
                data = json.load(f)
            handle_product_families_data(data)
        except Exception as E:
            print(E)
