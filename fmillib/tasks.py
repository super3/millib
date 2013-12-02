import urllib.request
import json
import time
import calendar

from celery import Celery
from celery.utils.log import get_task_logger

from db import connect_to_database

logger = get_task_logger(__name__)
app = Celery('tasks')


@app.task
def grab_ticker_usd(url):
    """
    downloads data through api
    """
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf8'))
        converted_data = convert_btc_log(data)
        insert_btc_log(converted_data)


def grab_bitstamp():
    url = 'https://www.bitstamp.net/api/ticker/'


def convert_btc_log(data):
    """
    Checks and converts (timestamp) data
    """
    for key in ('24h_avg', 'ask', 'bid', 'last', 'total_vol',):
        if not isinstance(data.get(key), float):
            raise IncorrectValue("Invalid price format")

    try:
        s_time = time.strptime(data['timestamp'], '%a, %d %b %Y %H:%M:%S -0000')
    except ValueError:
        raise IncorrectValue("Invalid datetime format")

    data['unix_timestamp'] = calendar.timegm(s_time)  # epoch time since 1970.1.1 in seconds

    return data


def insert_btc_log(data):
    """
    The api caches results. It updates a data with some interval, if we grab
    data more often than they update then we get same result. In order to avoid
    such duplication this code checks if we have already had an entry in the table.
    """

    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM btc_log WHERE ts=:ts", dict(ts=data['unix_timestamp']))
    already_inserted_for_this_ts = cur.fetchall()

    if not already_inserted_for_this_ts:
        cur.execute("""INSERT INTO btc_log ('id', '24h_avg', 'ask', 'bid', 'last',
                           'total_vol', 'ts') VALUES (NULL, :24h_avg, :ask, :bid,
                            :last, :total_vol, :ts)""",
                    {
                        '24h_avg': data['24h_avg'],
                        'ask': data['ask'],
                        'bid': data['bid'],
                        'last': data['last'],
                        'total_vol': data['total_vol'],
                        'ts': data['unix_timestamp']
                    })

        conn.commit()

    cur.close()
    conn.close()


class IncorrectValue(Exception):
    pass