source rosenv/bin/activate

gunicorn -k eventlet manage:app
