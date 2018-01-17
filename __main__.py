import logging, os
log_level = getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper())
logging.basicConfig(level = log_level)

from lib.server import run

if __name__ == '__main__':
    run()
