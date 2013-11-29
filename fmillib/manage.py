from flask.ext.script import Manager
from fmillib import app
import db

manager = Manager(app)

@manager.command
def init_db():
    """
    Creates the table for storing btc log
    """
    db.init_db()

if __name__ == "__main__":
    manager.run()