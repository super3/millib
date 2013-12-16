import datetime

from application import BitcoinAverageMapper
from application import BitstampMapper
from application import CampbxMapper
from application import MgtoxMapper
from application import Parser

CELERY_IMPORTS = ('tasks', )
CELERY_TIMEZONE = 'UTC'
BROKER_URL = 'redis://localhost:6379/0'
CELERYD_HIJACK_ROOT_LOGGER = False

bitstamp = Parser('https://www.bitstamp.net/api/ticker/')
campbx = Parser('http://campbx.com/api/xticker.php')
mtgox = Parser('http://data.mtgox.com/api/2/BTCUSD/money/ticker')
bitcoinaverage = Parser('https://api.bitcoinaverage.com/ticker/USD')

parsers = [bitstamp, campbx, mtgox, bitcoinaverage]
mappers = [BitstampMapper, CampbxMapper, MgtoxMapper, BitcoinAverageMapper]

CELERYBEAT_SCHEDULE = {
    'add-every-60-seconds': {
        'task': 'tasks.grab_btc_data',
        'schedule': datetime.timedelta(seconds=60),
        'args': (parsers, mappers)
    },
}
