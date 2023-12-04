from olist_view.management.commands.data_population_utils import load_data
from olist_view.models import EURUSDForex


def load_eurusd_forex_data(self):
    self.stdout.write(self.style.SUCCESS('Starting EUR-USD forex data population...'))

    csv_path = 'datasets/EURUSD_ForexTrading_4hrs_05.05.2003_to_16.10.2021.csv'
    load_data(EURUSDForex, csv_path, {}, {})

    self.stdout.write(self.style.SUCCESS('EUR-USD forex data loaded successfully.'))
