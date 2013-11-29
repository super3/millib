Millib[![Build Status](https://travis-ci.org/kaygorodov/millib.png?branch=master)](https://travis-ci.org/kaygorodov/millib)
======

A simplistic Bitcoin pricer checker website in mBTC.

Screenshots
-----------

![millib dashboard](https://github.com/kaygorodov/millib/raw/master/docs/images/screenshot_dashboard_main.png)

Installation
-----------

Install redis (It's used as a celery broker):

    $ sudo apt-get install redis-server


Python 3.3 for Ubuntu 12.04

    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python3.3

Create virtualenv for this project::

    $ virtualenv --python /usr/bin/python3.3 ~/env/millib

Be sure that you have virtualenv > 1.8.2 (Python 3.3.0 needs virtualenv 1.8.2)

    $ sudo pip install -U virtualenv

Install python dependencies::

    $ . ~/env/millib/bin/activate
    (millib) $ pip install -r requirements.txt --use-mirrors

Install node.js:

    sudo add-apt-repository ppa:chris-lea/node.js
    sudo apt-get update
    sudo apt-get install npm nodejs

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

    (millib) $ cd fmillib
    (millib) $ python manage.py init_db

That's it. Run the server::

    (millib) $ python fmillib.py

Run the celery::

    (millib) $ celery worker -B --loglevel INFO

Run tests (you must run in the fmillib directory):

    (millib) $ py.test


Run celery and flask server as services
-----------

* Flask: http://flask.pocoo.org/docs/deploying/
* Celery: http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html

