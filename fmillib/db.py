import sqlite3


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def connect_to_database():
    from fmillib import app
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = make_dicts
    return conn


def init_db(conn):
    from fmillib import app
    with app.app_context():
        with app.open_resource('schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()