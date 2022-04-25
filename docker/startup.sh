#!/bin/sh
./manage.py runserver_plus 0.0.0.0:8000
#if [[ "True" = "$DJANGO_DEBUG" ]]; then
#    ./manage.py runserver 0.0.0.0:8000
#else
#    gunicorn \
#        wsgi:application \
#        --bind 0.0.0.0:8000 \
#        --name root \
#        --user root \
#        --group root \
#        --timeout $GUNICORN_TIMEOUT \
#        --workers $GUNICORN_NUM_WORKERS \
#        --log-level $GUNICORN_LOG_LEVEL \
#        --forwarded-allow-ips "*" \
#        --log-file=-
#fi

