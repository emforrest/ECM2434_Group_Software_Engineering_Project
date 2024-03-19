import logging

# Create Custom Coloured Formatter
class ColouredFormat(logging.Formatter):
    
    # ANSI Escape Colours (https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit) + ANSI Reset String
    colours = {'yellow': "\x1b[38;5;220m",
               'red': "\x1b[38;5;9m",
               'blue': "\x1b[38;5;25m",
               'green': "\x1b[38;5;2m",
               "dark_red": "\x1b[38;5;124m"}
    reset = "\x1b[0m"

    # Set Colours For Logging Levels
    levelFormats = {logging.DEBUG:  colours['green'] + "[%(levelname)s]" + reset,
                    logging.INFO: colours['blue'] + "[%(levelname)s]" + reset,
                    logging.WARNING: colours['yellow'] + "[%(levelname)s]" + reset,
                    logging.ERROR: colours['red'] + "[%(levelname)s]" + reset,
                    logging.CRITICAL: colours['dark_red'] + "[%(levelname)s]" + reset}

    # Create Format Based On Inputted Record
    def format(self, record):
        logFormat = "%(asctime)s " + self.levelFormats.get(record.levelno) + " %(name)s"
        
        if record.levelno == logging.CRITICAL:
            logFormat += ": "+ self.colours['dark_red'] +"%(message)s"+ self.reset
        else:
            logFormat += ": %(message)s"
        
        formatter = logging.Formatter(logFormat, datefmt="%d-%m-%Y %H:%M:%S")
        return formatter.format(record)


# Config for the logging module
# https://docs.djangoproject.com/en/5.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "custom"
        },
        "master": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": "../logs/master.log",
            "mode": "a",
            "encoding": "UTF-8",
            "formatter": "custom"
        },
        "debug": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "../logs/debug.log",
            "mode": "a",
            "encoding": "UTF-8",
            "formatter": "custom"
        }
    },
    "formatters": {
        "custom": {
            "()": ColouredFormat
        }
    },
    "loggers": {
        "django": {
            "level": "DEBUG",
            "propagate": True,
        }
    },
    "root": {
        "handlers": ["console", "master", "debug"],
        "level": "DEBUG",
    }
} 