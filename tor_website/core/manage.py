#!/usr/bin/env python
"""Enhanced Django's command-line utility for administrative tasks."""
import os
import sys
import logging
from django.core.management import execute_from_command_line
from django.core.management.base import CommandError

def setup_logging():
    """Configure logging for management commands."""
    logger = logging.getLogger('django.management')
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('manage.log')

    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add to handlers
    c_format = logging.Formatter('%(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

def main():
    """Run administrative tasks with enhanced features."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger('django.management')

    # Handle environment variables for settings
    settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'core.settings')

    # Allow overriding settings module via command-line arguments
    if '--settings' in sys.argv:
        settings_index = sys.argv.index('--settings')
        if settings_index + 1 < len(sys.argv):
            settings_module = sys.argv[settings_index + 1]
        else:
            logger.error("No settings module specified after --settings.")
            sys.exit(1)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.error(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        execute_from_command_line(sys.argv)
    except CommandError as e:
        logger.error(f"CommandError: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        sys.exit(1)

if __name__ == '__main__':
    main()
