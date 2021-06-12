web: gunicorn FakeCSV.wsgi --log-file -
worker: celery -A FakeCSV worker -l INFO