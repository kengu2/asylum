# -*- coding: utf-8 -*-
import datetime
import itertools

import dateutil.parser
from django.core.management.base import BaseCommand, CommandError
from holviapp.importer import HolviImporter
from holviapp.utils import list_invoices, list_orders


def yesterday_proxy():
    now_yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    start_yesterday = datetime.datetime.combine(now_yesterday.date(), datetime.datetime.min.time())
    return start_yesterday.isoformat()


class Command(BaseCommand):
    help = 'Import transaction data from Holvi API'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Import all Holvi transactions (WARNING: this may take forever)')
        parser.add_argument('since', type=str, nargs='?', default=yesterday_proxy(), help='Import transactions updated since datetime, defaults to yesterday midnight')

    def handle(self, *args, **options):
        if (not options['since']
                and not options['all']):
            raise CommandError('Either since or all must be specified')
        invoice_filters = {}
        order_filters = {}
        if not options.get('all', False):
            since_parsed = dateutil.parser.parse(options['since'])
            if options['verbosity'] > 1:
                print("Importing since %s" % since_parsed.isoformat())
            invoice_filters['update_time_from'] = since_parsed.isoformat()
            order_filters['filter_paid_time_from'] = since_parsed.isoformat()

        h = HolviImporter(itertools.chain(list_invoices(**invoice_filters), list_orders(**order_filters)))
        transactions = h.import_transactions()
        if options['verbosity'] > 1:
            for t in transactions:
                print("Imported transaction %s" % t)
