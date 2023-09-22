import json
import sys

XREF_FILE_NAME = "xref-products.json"
OUT_FILE = "xref-products.jsonl"


def build_json_obj(index_name):
    if index_name == "xref":
        try:
            with open(XREF_FILE_NAME, ) as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(e)


def convert_json_to_jsonl(json_obj):
    try:
        with open(OUT_FILE, 'w') as file:
            for entry in json_obj:
                json.dump(entry, file)
                file.write("\n")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    index_name = sys.argv[1]
    convert_json_to_jsonl(build_json_obj(index_name))
