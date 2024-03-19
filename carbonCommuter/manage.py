#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Create logs directory if one is missing
    if not("logs" in os.listdir("..")):
        os.mkdir("../logs")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbonCommuter.settings')
    if sys.argv[1] == "backuplogs":
        os.environ.setdefault('DJANGO_LOGGING', 'False')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
