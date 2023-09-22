from ses.algolia import Products, ProductsIndex
import click


@click.command(options_metavar='<options>', short_help='Produce search index entries')
@click.option('--directory', required=True, help='path to directory', metavar='<string>')
def products(directory):
    """
    Produce products index data from a directory of json files generated from products cdn=json
    """
    ProductsIndex(directory)
