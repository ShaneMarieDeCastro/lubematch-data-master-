from cli.sql import commands as sql_commands
from cli.products import commands as products_commands
from cli.entities import commands as entities_commands
from cli.algolia import commands as algolia_commands
import click
import json
import os


@click.group()
def cli():
    """
    SES CLI provides commands to generate data from raw data
    used to populate SES databases for Solutions Hub and LubeChat
    """
    pass


@cli.group()
def sql():
    """
    Commands to get Shell data into sqlite

    Commands essentially add tables to a given sqlite file
    """
    pass


sql.add_command(sql_commands.gpc)
sql.add_command(sql_commands.xref)
sql.add_command(sql_commands.tdg)
sql.add_command(sql_commands.o2n)
# sql.add_command(sql_commands.specs_lookup)
# sql.add_command(sql_commands.specs_product)
sql.add_command(sql_commands.material_codes)
sql.add_command(sql_commands.carbon_neutral)
sql.add_command(sql_commands.grade_names)
sql.add_command(sql_commands.fluid_type)
sql.add_command(sql_commands.fluid_subtype)
sql.add_command(sql_commands.sub_groups)
sql.add_command(sql_commands.packshot)
sql.add_command(sql_commands.dvr)
sql.add_command(sql_commands.commerce)


@cli.group()
def products():
    """
    Commands to get Shell product data
    """
    pass


products.add_command(products_commands.all)
products.add_command(products_commands.xref)
products.add_command(products_commands.items)
products.add_command(products_commands.o2n)


@cli.group()
def entities():
    """
    Commands to generate entities
    """
    pass


entities.add_command(entities_commands.names)


@cli.group()
def algolia():
    """
    Commands to generate algolia search entities
    """
    pass


algolia.add_command(algolia_commands.products)
