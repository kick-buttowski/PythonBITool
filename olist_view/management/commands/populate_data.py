from django.core.management.base import BaseCommand

from olist_view.management.commands.populate_eurusd_forex_data import load_eurusd_forex_data
from olist_view.management.commands.populate_gamestop_data import load_gamestop_date
from olist_view.management.commands.populate_olist_data import load_olist_data


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting olist data population...'))
        load_olist_data(self)
        self.stdout.write(self.style.SUCCESS('Olist data loaded successfully.'))

        # load_eurusd_forex_data()

        self.stdout.write(self.style.SUCCESS('Starting GameStop stock data population...'))
        load_gamestop_date(self)
        self.stdout.write(self.style.SUCCESS('GameStop stock data loaded successfully.'))
