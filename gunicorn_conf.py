wsgi_app = "lib.wsgi:application"
bind = "127.0.0.1:8000"
reaload = True
accesslog = errorlog = "/lib/gunicorn.log"
capture_output = True
daemon = True
workers = 6
pidfile = "/lib/gunicorn_pid"