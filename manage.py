#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
import stockbroker_service.glo as glob

sys.argv = []
sys.argv.extend([".\\manage.py"])
sys.argv.extend(["runserver"])
sys.argv.extend(["0.0.0.0:8000"])


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockbroker_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print(sys.argv)
    glob._init()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # python manage.py runserver 0.0.0.0:8000
    main()
