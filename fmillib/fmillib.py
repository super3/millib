import calendar
import datetime

from flask import Flask
from flask import g
from flask import jsonify
from flask import request
from flask import render_template

app = Flask(__name__, static_folder='../static', static_url_path='', template_folder='../static/app')
app.config.from_object('default_settings')
app.config.from_envvar('FMILLIB_SETTINGS', silent=True)


@app.route('/')
def index():
    return render_template('index.html', name='index')


@app.route('/get_btc_logs', methods=['POST'])
def get_btc_logs():
    """
    Returns the btc_logs from "since" to now.
    If "since" is less than (now - NUM_OF_DAYS) then It returns btc_logs
    for the last NUM_OF_DAYS days
    """
    NUM_OF_DAYS = 90
    MAX_OF_BTC_LOGS = 400
    since = int(request.json.get('since', 0))

    min_time = datetime.datetime.now() - datetime.timedelta(days=NUM_OF_DAYS)
    min_time_ts = calendar.timegm(min_time.utctimetuple())

    if since < min_time_ts:
        since = min_time_ts

    cur = g.database.execute("SELECT * FROM btc_log WHERE ts>:since ORDER BY ts DESC LIMIT :limit",
                       dict(since=since, limit=MAX_OF_BTC_LOGS))
    rv = cur.fetchall()
    cur.close()
    rv.reverse()
    return jsonify({'btc_logs': rv})


@app.before_request
def before_request():
    import db
    g.database = db.connect_to_database()


@app.teardown_request
def teardown_request(exception):
    database = getattr(g, 'db', None)
    if database is not None:
        database.close()

if __name__ == '__main__':
    app.run()
