from ses.names import Names
import click


@click.command(options_metavar='<options>', short_help='Get all product names for a given <country>')
@click.argument('country', metavar='<country>')
@click.option('--sqlite', default='data/ses.sqlite', help='path to sqlite database', metavar='<string>')
def names(country, sqlite):
    """
    Get all product names for a given <country>
    """
    n = Names(sqlite, country)
    n.shell()
    n.close()
