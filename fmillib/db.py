import sqlite3
from fmillib import app


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def connect_to_database():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = make_dicts
    return conn


def init_db():
    conn = connect_to_database()
    with app.app_context():
        with app.open_resource('schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()
    conn.close()