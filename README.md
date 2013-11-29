Millib - Phase One
======
A simplistic Bitcoin pricer checker website in mBTC.

Screenshots
-----------

![millib dashboard](https://github.com/kaygorodov/millib/raw/master/docs/images/screenshot_dashboard.png)

Installation
-----------

Install redis (It's used as a celery broker):

    $ sudo apt-get install redis-server

Create virtualenv for this project::

    $ virtualenv --python /usr/bin/python3.3 ~/env/millib

Install python dependencies::

    $ . ~/env/millib/bin/activate
    (millib) $ pip install -r requirements.txt --use-mirrors

Install bower (http://bower.io/)::

    $ sudo npm install bower -g

Go to project's static folder and install all frontend dependencies::

    $ cd static
    $ bower install

Create your own settings file::

    # my_settings.py
    # you should set ENVVAR FMILLIB_SETTINGS=<path to your settings file>
    # for example for me
    # export FMILLIB_SETTINGS='/home/kaygrodov/projects/millib/fmillib/my_settings.py'

    DATABASE = '/home/kaygrodov/projects/millib/fmillib/fmillib.db' # path to your database
    DEBUG = True

Set virtual env variable (It depends how you run project. You can do this through supervisor.).
If you just want to run server in console then::

    (millib) $ export FMILLIB_SETTINGS=<path to your file>

Init database::

    (millib) $ python manage.py init_db

That's it. Run the server::

    (millib) $ python fmillib.py

Run the celery::

    (millib) $ celery worker -B --loglevel INFO


Run celery and flask server as services
-----------

* Flask: http://flask.pocoo.org/docs/deploying/
* Celery: http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html

