MilliB([![Build Status](https://travis-ci.org/kaygorodov/millib.png?branch=master)](https://travis-ci.org/kaygorodov/millib))
======

A simplistic Bitcoin pricer checker website in mBTC. 

Screenshot
-----------

![millib dashboard](https://github.com/kaygorodov/millib/raw/master/docs/images/screenshot_dashboard_main.png)

Installation Guide
-----------

Install redis (It's used as a celery broker):

    $ sudo apt-get install redis-server


Python 3.3 for Ubuntu 12.04

    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python3.3

Create virtualenv for this project:

    $ virtualenv --python /usr/bin/python3.3 ~/env/millib

Be sure that you have virtualenv > 1.8.2 (Python 3.3.0 needs virtualenv 1.8.2)

    $ sudo pip install -U virtualenv

Install python dependencies:

    $ . ~/env/millib/bin/activate
    (millib) $ pip install -r requirements.txt --use-mirrors

Install node.js:

    sudo add-apt-repository ppa:chris-lea/node.js
    sudo apt-get update
    sudo apt-get install npm nodejs

Install [bower](http://bower.io):

    $ sudo npm install bower -g

Go to project's static folder and install all frontend dependencies:

    $ cd static
    $ bower install

Create your own settings file:

    # my_settings.py
    # you should set ENVVAR FMILLIB_SETTINGS=<path to your settings file>
    # for example for me
    # export FMILLIB_SETTINGS='/home/kaygrodov/projects/millib/fmillib/my_settings.py'

    DATABASE = '/home/kaygrodov/projects/millib/fmillib/fmillib.db' # path to your database
    DEBUG = True

Set virtual env variable (It depends how you run project. You can do this through supervisor.).
If you just want to run server in console then:

    (millib) $ export FMILLIB_SETTINGS=<path to your file>

Init database:

    (millib) $ cd fmillib
    (millib) $ python manage.py init_db

That's it. Run the server:

    (millib) $ python fmillib.py

Run the celery:

    (millib) $ celery worker -B --loglevel INFO

Run tests (you must run in the fmillib directory):

    (millib) $ py.test


Run celery and flask server as services
-----------

* Flask: http://flask.pocoo.org/docs/deploying/
* Celery: http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html

Add a supervisor conf file for gunicorn:

    root@millib:/etc# cat /etc/supervisor/conf.d/gunicorn_millib.conf

    [program:millib]
    command = /var/www/env/millib/bin/gunicorn -b 127.0.0.1:9999 --pythonpath /var/www/millib/fmillib/ fmillib:app
    user = www-data
    stdout_logfile = /var/www/gunicorn_millib_supervisor.log
    redirect_stderr = true

Start service:

    root@millib:/etc# supervisorctl start millib
    millib: started

Add nginx proxy from 80 port to 9999:

    location / {
        proxy_pass       http://localhost:8000;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

Add a supervisor conf file for celery:

    root@millib:/etc# cat /etc/supervisor/conf.d/celery_millib.conf
    [program:celery]
    command = /var/www/env/millib/bin/celery worker -B --loglevel INFO --workdir=/var/www/millib/fmillib/
    user = www-data
    stdout_logfile = /var/www/celery_millib_supervisor.log
    redirect_stderr = true

Start the service:

    root@millib:/etc# supervisorctl start millib
    millib: started

That's it.
