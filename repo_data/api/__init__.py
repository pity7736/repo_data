from logging.config import dictConfig

from .main import app  # noqa: F401

LOG_CONFIG = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'general': {
            'format': '%(levelname)s | %(asctime)s | %(filename)s | function name: '
                      '%(funcName)s | line number: %(lineno)d | %(message)s'
        },
    },
    'handlers': {
        'general': {
            'level': 'DEBUG',
            'formatter': 'general',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'repo_data': {
            'handlers': ('general',),
            'level': 'DEBUG'
        }
    },
}

dictConfig(LOG_CONFIG)
