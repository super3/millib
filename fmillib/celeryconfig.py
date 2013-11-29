from datetime import timedelta

URL = "https://api.bitcoinaverage.com/ticker/USD"

CELERYBEAT_SCHEDULE = {
    'add-every-60-seconds': {
        'task': 'tasks.grab_ticker_usd',
        'schedule': timedelta(seconds=60),
        'args': (URL, )
    },
}

CELERY_IMPORTS = ('tasks', )
CELERY_TIMEZONE = 'UTC'
BROKER_URL = 'redis://localhost:6379/0'
CELERYD_HIJACK_ROOT_LOGGER = False