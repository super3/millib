# Requirements

- Python 3
- Redis
- LXML

# Installation

- [Python 3](http://www.python.org/download/)
- apt-get install libxml2-dev libxslt-dev
- Clone repository
- Make new virtualenv environment
- Activate created environment
- Install requirements from requirements.txt (pip install -r requirements.txt)

# Run Application

- Run celery worker (celery worker -b --loglevel INFO)
- Run application (python application.py)
