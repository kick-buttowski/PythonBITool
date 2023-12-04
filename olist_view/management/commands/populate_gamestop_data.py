from olist_view.management.commands.data_population_utils import load_data
from olist_view.models import GameStopStockData, GameStopAlias


def load_gamestop_date(cls):
    csv_path = 'datasets/GME_stock.csv'
    load_data(cls, GameStopStockData, csv_path, {}, {})

    aliases_csv_path = 'datasets/gamestop_aliases.csv'
    load_data(cls, GameStopAlias, aliases_csv_path, {}, {})