from ses.gpc import gpc_tables
from ses.xref import xref_table
from ses.tdg import tdg_table
from ses.o2n import o2n_table
from ses.material_codes import material_codes_table
from ses.carbon_neutral import carbon_neutral_table
from ses.grades import grade_names_table
from ses.fluid_types import base_oil_sub_group_table
from ses.fluid_types import base_oil_group_table
from ses.sub_groups import sub_group_i18n
from ses.packshots import packshot_table
from ses.dvr import dvr_table
from ses.commerce import commerce_table
# from ses.specs import specs_lookup_table, specs_product_table
import click


@click.command(options_metavar='<options>', short_help='Add the GPC tables to sqlite')
@click.option('--connection', required=True, help='GPC connection string', metavar='<string>')
@click.option('--sqlite', default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def gpc(connection, sqlite):
    """
    Add lubechat tables from GPC to a <sqlite> database

    Must be on Shell VPN
    """
    gpc_tables(connection, sqlite)


@click.command(options_metavar='<options>', short_help='Add the XREF table to sqlite')
@click.option('--path',  required=True, help='Path to XREF xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def xref(path, sqlite):
    """
    Add the XREF table to <sqlite> database
    """
    xref_table(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the TDG table to sqlite')
@click.option('--api_key',  required=True, help='Key for signals API', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def tdg(api_key, sqlite):
    """
    Add the TDG table to <sqlite> database
    """
    tdg_table(api_key, sqlite)


@click.command(options_metavar='<options>', short_help='Add the Old to New data to sqlite')
@click.option('--path',  required=True, help='Path to Old2New csv file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def o2n(path, sqlite):
    """
    Add the OLD2NEW table to <sqlite> database
    """
    o2n_table(path, sqlite)


# @click.command(options_metavar='<options>', short_help='Add the specs lookup data to sqlite')
# @click.option('--path',  required=True, help='Path to specs csv file', metavar='<string>')
# @click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
# def specs_lookup(path, sqlite):
#     """
#     Add the SPECS_LOOKUP table to <sqlite> database
#     """
#     specs_lookup_table(path, sqlite)


# @click.command(options_metavar='<options>', short_help='Add the specs product data to sqlite')
# @click.option('--path',  required=True, help='Path to specs product xlsx file', metavar='<string>')
# @click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
# def specs_product(path, sqlite):
#     """
#     Add the SPECS_PRODUCT table to <sqlite> database
#     """
#     specs_product_table(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the material code data to sqlite')
@click.option('--path',  required=True, default='data/material_codes.xlsx', help='Path to material codes xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def material_codes(path, sqlite):
    """
    Add the MATERIAL_CODES table to <sqlite> database
    """
    material_codes_table(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the carbon neutral products data to sqlite')
@click.option('--path',  required=True, default='data/carbon_neutral.xlsx', help='Path to carbon neutral products xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def carbon_neutral(path, sqlite):
    """
    Add the carbon neutral products table to <sqlite> database
    """
    carbon_neutral_table(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the product viscosity grade type names data to sqlite')
@click.option('--path',  required=True, default='data/grade_name.xlsx', help='Path to updated viscosity grade names xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def grade_names(path, sqlite):
    """
    Add the grade name corrections table to <sqlite> database
    """
    grade_names_table(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the base oil sub types data to sqlite')
@click.option('--path',  required=True, default='data/fluid_sub_groups.xlsx', help='Path to updated base oil subtype names xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def fluid_subtype(path, sqlite):
    """
    Add the base oil sub types table to <sqlite> database
    """
    base_oil_sub_group_table(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the base oil types data to sqlite')
@click.option('--path',  required=True, default='data/fluid_groups.xlsx', help='Path to updated base oil type names xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def fluid_type(path, sqlite):
    """
    Add the base oil types table to <sqlite> database
    """
    base_oil_group_table(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the sub group names data to sqlite')
@click.option('--path',  required=True, default='data/sub_group_i18n.xlsx', help='Path to sub group names xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def sub_groups(path, sqlite):
    """
    Add the product subgroups table to <sqlite> database
    """
    sub_group_i18n(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the packshot url data to sqlite')
@click.option('--path',  required=True, default='data/packshots.xlsx', help='Path to packshots url xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def packshot(path, sqlite):
    """
    Add the packshot URL table to <sqlite> database
    """
    packshot_table(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the dvr data to sqlite')
@click.option('--path',  required=True, default='data/dvr.xlsx', help='Path to dvr xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def dvr(path, sqlite):
    """
    Add the DVRs table to <sqlite> database
    """
    dvr_table(path, sqlite)


@click.command(options_metavar='<options>', short_help='Add the ecommerce link data to sqlite')
@click.option('--path',  required=True, default='data/commerce.xlsx', help='Path to ecommerce link xlsx file', metavar='<string>')
@click.option('--sqlite',  default='data/ses.sqlite', help='Path to sqlite database file', metavar='<string>')
def commerce(path, sqlite):
    """
    Add the ecommerce table to <sqlite> database
    """
    commerce_table(path, sqlite)
