import urllib.request
import datetime
import calendar
import logging
import socket
import time
import json
import re

import lxml.html

from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template
from flask import jsonify
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/bitcoins')
def bitcoins():
    row = Bitcoin.query.all()
    row2dict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}
    btc = list(map(row_to_dict, row))

    return jsonify({'bitcoins': btc})


@app.route('/tables')
def table():
    coin_market_parser = CoinMarketCapParser()

    return render_template('tables.html', data=coin_market_parser.get_data())


def row_to_dict(row):
    temp = {}
    for column in row.__table__.columns:
        current = getattr(row, column.name)
        logger.debug(current)

        if type(getattr(row, column.name)) is datetime.datetime:
            temp[column.name] = calendar.timegm(current.utctimetuple())
        else:
            temp[column.name] = name=current

    return temp


class Bitcoin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Float, nullable=False)
    ask = db.Column(db.Float, nullable=False)
    last = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, nullable=False)
    day_average = db.Column(db.Float)
    total_vol = db.Column(db.Float)

    def __init__(self, bid, ask, last, timestamp, day_average, total_vol):
        self.bid = bid
        self.ask = ask
        self.last = last
        self.timestamp = timestamp
        self.day_average = day_average
        self.total_vol = total_vol

    def __repr__(self):
        return '<Bitcoin ask:{ask}, bid:{bid}>'.format(ask=self.ask, bid=self.bid)


class Parser(object):
    def __init__(self, url):
        self.url = url

    def fetch(self):
        request = urllib.request.Request(self.url)
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0')

        try:
            return urllib.request.urlopen(request, timeout=5).read().decode('utf-8')
        except socket.timeout:
            logger.error('Timed out url: %s', self.url)
            return None

    def jsonify(self, response):
        if response:
            logger.info('API Response: %s', response)
            return json.loads(response)


class Mapper(object):
    def __init__(self):
        self.bid = None
        self.ask = None
        self.last = None
        self.timestamp = None
        self.day_average = None
        self.total_vol = None


class BitstampMapper(Mapper):
    def __init__(self, content):
        super(BitstampMapper, self).__init__()

        self.bid = content.get('bid')
        self.ask = content.get('ask')
        self.last = content.get('last')
        self.timestamp = datetime.datetime.fromtimestamp(int(content.get('timestamp')))
        self.total_vol = content.get('volume')


class CampbxMapper(Mapper):
    def __init__(self, content):
        super(CampbxMapper, self).__init__()

        self.bid = content.get('Best Bid')
        self.ask = content.get('Best Ask')
        self.last = content.get('Last Trade')
        self.timestamp = datetime.datetime.now()


class BitcoinAverageMapper(Mapper):
    def __init__(self, content):
        super(BitcoinAverageMapper, self).__init__()

        self.bid = content.get('bid')
        self.ask = content.get('ask')
        self.last = content.get('last')

        struct_time = time.strptime(content.get('timestamp'), '%a, %d %b %Y %H:%M:%S -0000')
        self.timestamp = datetime.datetime.fromtimestamp(time.mktime(struct_time))

        self.day_average = content.get('24h_avg')
        self.total_vol = content.get('total_vol')


class MgtoxMapper(Mapper):
    def __init__(self, content):
        super(MgtoxMapper, self).__init__()

        content = content.get('data')

        self.bid = content.get('sell')['value']
        self.ask = content.get('buy')['value']
        self.last = content.get('last')['value']
        self.timestamp = datetime.datetime.now()
        self.day_average = content.get('avg')['value']
        self.total_vol = content.get('vol')['value']


class CryptoCurrencyParser(object):
    def __init__(self, currency):
        self.currency = currency
        self.doc = lxml.html.parse('http://coinmarketcap.com/')

    @property
    def total_supply(self):
        xpath = '//table[@id="currencies"]/tr[contains(., "%s")]/td[5]/text()' % self.currency
        return self.doc.xpath(xpath)[0]

    @property
    def usd_price(self):
        xpath = '//table[@id="currencies"]/tr[contains(., "%s")]/td[4]/a[@class="price-usd"]/text()' % self.currency
        return self.doc.xpath(xpath)[0]

    @property
    def btc_price(self):
        xpath = '//table[@id="currencies"]/tr[contains(., "%s")]/td[4]/a[@class="price-btc"]/text()' % self.currency
        return self.doc.xpath(xpath)[0]

    @property
    def market_cap(self):
        xpath = '//table[@id="currencies"]/tr[contains(., "%s")]/td[3]/div[@class="market-cap-usd"]/text()' % self.currency
        return self.doc.xpath(xpath)[0]


class CoinMarketCapParser(object):
    def __init__(self):
        self.float_extract = re.compile(r'\d+.\d+')
        self.integer_extract = re.compile(r'\d+.')

        self.doc = lxml.html.parse('http://coinmarketcap.com/')
        self.table_rows = self.doc.xpath('//table[@id="currencies"]/tr')

        del(self.table_rows[0])  # Delete captions.

        logger.info('self.doc: %s', self.doc)
        logger.info('self.table_rows: %s', self.table_rows)

    def get_data(self):
        for table_row in self.table_rows:
            try:
                yield dict(name=self._name(table_row), total_supply=self._total_supply(table_row), usd_price=self._usd_price(table_row),
                           btc_price=self._btc_price(table_row), market_cap=self._market_cap(table_row),
                           icon='http://coinmarketcap.com/' + self._icon(table_row))
            except IndexError:
                logger.info('Fail with row: %s', table_row)

    def _name(self, row):
        return row.xpath('td[2]/a/text()')[0]

    def _total_supply(self, row):
        extracted_data = row.xpath('td[5]/text()')[0].replace(',', '')

        return int(self.integer_extract.findall(extracted_data)[0])

    def _usd_price(self, row):
        extracted_data = row.xpath('td[4]/a[@class="price-usd"]/text()')[0]

        return float(self.float_extract.findall(extracted_data)[0])

    def _btc_price(self, row):
        extracted_data = row.xpath('td[4]/a[@class="price-btc"]/text()')[0].replace(',', '')

        return float(self.float_extract.findall(extracted_data)[0])

    def _market_cap(self, row):
        extracted_data = row.xpath('td[3]/div[@class="market-cap-usd"]/text()')[0].replace(',', '')

        return int(self.integer_extract.findall(extracted_data)[0])

    def _icon(self, row):
        return row.xpath('td[2]/img/@src')[0]

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5050)

    t = CryptoCurrencyParser('Bitcoin')

    logger.debug(t.total_supply)
    logger.debug(t.usd_price)
    logger.debug(t.btc_price)
    logger.debug(t.market_cap)

    coin_market_parser = CoinMarketCapParser()

    for i in coin_market_parser.get_data():
        print(i)