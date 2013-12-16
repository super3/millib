import logging

from celery import task

from application import Bitcoin
from application import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@task
def grab_btc_data(parsers, mappers):
    for parser, mapper in zip(parsers, mappers):
        logger.debug('Parser: %s\nMapper: %s', parser, mapper)
        response = parser.fetch()

        if response is None:
            continue

        try:
            content = parser.jsonify(response)
        except ValueError:
            content = None
            logger.warning('Somethig wrong with loading: %s', parser.url)

        if content is None:
            continue

        m = mapper(content)

        bitcoin = Bitcoin(m.bid, m.ask, m.last, m.timestamp, m.day_average, m.total_vol)
        db.session.add(bitcoin)
        db.session.commit()