from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from db import connect_to_database, init_db

app = Flask(__name__, static_folder='../static', static_url_path='')
DATABASE = 'fmillib.db'
DEBUG = True
app.config.from_object(__name__)

init_db(connect_to_database())

@app.route('/')
def root():
    return app.send_static_file('app/index.html')


@app.before_request
def before_request():
    g.db = connect_to_database()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()
