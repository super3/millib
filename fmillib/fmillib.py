from flask import Flask, g, jsonify, request
import calendar
import datetime

app = Flask(__name__, static_folder='../static', static_url_path='')
app.config.from_object('default_settings')
app.config.from_envvar('FMILLIB_SETTINGS', silent=True)


@app.route('/')
def root():
    return app.send_static_file('app/index.html')


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

    cur = g.db.execute("SELECT * FROM btc_log WHERE ts>:since ORDER BY ts DESC LIMIT :limit",
                       dict(since=since, limit=MAX_OF_BTC_LOGS))
    rv = cur.fetchall()
    cur.close()
    rv.reverse()
    return jsonify({'btc_logs': rv})


@app.before_request
def before_request():
    from db import connect_to_database
    g.db = connect_to_database()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()
