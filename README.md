# SES SQLite

We use SQLite to process a lot of the data needed to SES from source data

## Building the SQL file

If the --sqlite param e.g: `--sqlite=data/ses.sqlite` is omitted then the command will attempt to create ses.sqlite in data folder. This folder must exist.

### GPC

**Must be on the Shell VPN on a GID laptop with GPC approval**

This will clone all the required tables from the LUBCHT views in the IFGPC_DATA_LAYER schema in GPC production

**NOTE**: This command can take around 8 minutes to run

    ses-cli sql gpc --connection="<oracle connection string>"

### XREF

This command requireds a `global_xref.xlsx` file which is downloaded from sharepoint.

Contact [alex.bell@shell.com](mailto:alex.bell@shell.com?subject=SES%20CLI%20help) for more information.

    ses-cli sql xref --path="<path to global_xref.xlsx>"

### TDG

This command requires a TDG key to download the data required from the SIGNALS API. API Key= FB5C83957847A6D6862807A86EACF9AA

**NOTE**: This command can take around 4 minutes to run

Contact [alex.bell@shell.com](mailto:alex.bell@shell.com?subject=SES%20CLI%20help) for more information.

    ses-cli sql tdg --api_key='<API Key>'

---

### Old to New

This command required the `o2n.xlsx` file which is downloaded from sharepoint.

Contact [alex.bell@shell.com](mailto:alex.bell@shell.com?subject=SES%20CLI%20help) for more information.

    ses-cli sql o2n --path='<path to o2n.xlsx>'

### Specs lookup

This command required the `global_specs_parent_child_lookup.xlsx` file which is downloaded from sharepoint.

Contact [alex.bell@shell.com](mailto:alex.bell@shell.com?subject=SES%20CLI%20help) for more information.

    ses-cli sql specs-lookup --path='<path to global_specs_parent_child_lookup.xlsx>'

### Specs product

This command required the `specs_product.xlsx` file which is downloaded from sharepoint.

Contact [alex.bell@shell.com](mailto:alex.bell@shell.com?subject=SES%20CLI%20help) for more information.

    ses-cli sql specs-product --path='<path to spec_product.xlsx>'

### Material codes

This command required the `material_codes.xlsx` file which is downloaded from sharepoint.

Contact [alex.bell@shell.com](mailto:alex.bell@shell.com?subject=SES%20CLI%20help) for more information.

    ses-cli sql material-codes --path='<path to material_codes.xlsx>'

## Generating documents

We can generate the documents suitable for uploading to a CDN or just output to json.

**Note:** It can take about 65 minutes to run for all the languages on python. This is due to the performance of the python sqlite3 driver.

    ses-cli products all en-AU --out cdn &
    ses-cli products all en-CA --out cdn &
    ses-cli products all fr-CA --out cdn &
    ses-cli products all en-GB --out cdn &
    ses-cli products all en-IN --out cdn &
    ses-cli products all en-MY --out cdn &
    ses-cli products all en-SG --out cdn &
    ses-cli products all en-US --out cdn &
    ses-cli products all zh-CN --out cdn &
    ses-cli products all id-ID --out cdn &
    ses-cli products all de-DE --out cdn &
    ses-cli products all ru-RU --out cdn &
    ses-cli products all en-PH --out cdn &
    ses-cli products all en-IE --out cdn

## Generating xref

Generates xref file for all products

    ses-cli products xref > xref.json
    
    
## Loading documents into Typesense

Loads the documents for a specific index into the server, either local or remote
``` 
python3 loadIndex.py <local/remote> <products/old2new/xref/product-families/all> 
```
