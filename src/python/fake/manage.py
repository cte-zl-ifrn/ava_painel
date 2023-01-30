#!/usr/bin/env python
import os
import sys
from settings import DATABASES
import psycopg2
import time
import logging


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("ops!") from exc

    if len(sys.argv) > 1 and sys.argv[1] in ['runserver', 'runserver_plus']:
        db = DATABASES['default']
        connection = psycopg2.connect(
            dbname=db['NAME'],
            user=db['USER'],
            password=db['PASSWORD'],
            host=db['HOST'],
            port=db['PORT']
        )
        while connection.closed:
            logging.info(f"ERROR: Aguardando o banco {db['HOST']:db['PORT']/db['NAME']} subir")
            time.sleep(3)
        execute_from_command_line([sys.argv[0], 'migrate'])
        
    execute_from_command_line(sys.argv)
