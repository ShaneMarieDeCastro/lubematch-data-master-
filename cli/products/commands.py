from ses.products import ProductsPacksDocs, ProductsPerCountry
from ses.xref import xref_products
from ses.o2n import o2n_products
import click
import os
import json


@click.command(options_metavar='<options>', short_help='Get all products')
@click.argument('locale', metavar='<locale>')
@click.option('--sqlite', default='data/ses.sqlite', help='path to sqlite database', metavar='<string>')
@click.option('--sub_groups', default='data/sub_group_i18n.xlsx', help='path to sub_groups translations', metavar='<string>')
@click.option('--marketing', default='data/short_marketing.xlsx', help='path to marketing translations', metavar='<string>')
@click.option('--phys', default='data/phys_char.xlsx', help='path to physical characteristics translations', metavar='<string>')
@click.option('--specs', default='data/global_specs_parent_child_lookup.xlsx', help='path to specs', metavar='<string>')
@click.option('--packs', default='data/pack_sizes.xlsx', help='path to packs', metavar='<string>')
@click.option('--out', default='json', help='output format json|cdn', metavar='<string>')
@click.option('--apps', default='data/attributes.xlsx', help='path to application keys data', metavar='<string>')
@click.option('--dvrs', default='data/dvr.xlsx', help='path to dvr data', metavar='<string>')
#@click.option('--commerce', default='data/commerce.xlsx', help='path to e-commerce data', metavar='<string>')
def all(locale, sqlite, sub_groups, marketing, phys, specs, packs, out, apps, dvrs):
    """
    Get all products in a given <locale> with pack sizes and
    Local TDS/SDS and Global TDS/SDS
    """

    print("Processing product data for: " + locale)
    p = ProductsPacksDocs(sqlite, sub_groups, marketing, phys, specs, packs, locale, apps, dvrs)
    products = p.lube_products()

    if out == 'json':
        print(json.dumps(products, ensure_ascii=False).encode('utf8').decode())
    if out == 'cdn':
        for k, v in products.items():
            filename = './out/{locale}/{code}.json'.format(
                locale=locale, code=k)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w", encoding='utf8') as f:
                f.write(json.dumps(v, indent=2, ensure_ascii=False).encode(
                    'utf8').decode())
    print("Finished: " + locale)
    p.close()


@click.command(options_metavar='<options>', short_help='Get all xref products for a given <country>')
@click.option('--sqlite', default='data/ses.sqlite', help='path to sqlite database', metavar='<string>')
def xref(sqlite):
    """
    Get all xref products with details, for a given <country>.
    """
    p = xref_products(sqlite)
    print(json.dumps(p, ensure_ascii=False).encode('utf8').decode())


@click.command(options_metavar='<options>', short_help='Get all products for a given <country>')
@click.argument('country', metavar='<country>')
@click.option('--sqlite', default='data/ses.sqlite', help='path to sqlite database', metavar='<string>')
def items(country, sqlite):
    """
    Get all products with details, for a given <country>.
    Only contains basic info for each product
    """
    p = ProductsPerCountry(sqlite, country)
    p.lube_products()
    p.close()


@click.command(options_metavar='<options>', short_help='Get all o2n products for a given <country>')
@click.option('--sqlite', default='data/ses.sqlite', help='path to sqlite database', metavar='<string>')
def o2n(sqlite):
    """
    Get all o2n products with details, for a given <country>.
    """
    p = o2n_products(sqlite)
    print(json.dumps(p, ensure_ascii=False).encode('utf8').decode())
