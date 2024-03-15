import os
import logging
from zipfile import ZipFile


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


# Backup last session log files into zip format

def backup_logs():
    # Set the maximum number of backups to keep
    MAX_BACKUPS = 10
    
    # Create a backups directory to store the zip files if one doesn't already exist
    if not("backups" in os.listdir("../logs")):
            os.mkdir("../logs/backups")
    
    # Loop through backups folder in reverse order, incrementing each session record
    if "master.log" in os.listdir("../logs/"):
            sortedFiles = sorted(os.listdir("../logs/backups"), key = lambda x: int(x.split(".")[1]) if x.split(".")[1].isdecimal() else 0, reverse=True)
            for file in sortedFiles:
                if file != "session.zip":
                    count = int(file.split(".")[1])
                    if count >= MAX_BACKUPS:
                        os.remove(f"../logs/backups/{file}")
                    else:
                        os.rename(f"../logs/backups/{file}", f"../logs/backups/session.{count+1}.zip")
            if "session.zip" in "../logs/backups/":
                os.rename("../logs/backups/session.zip", "../logs/backups/session.1.zip")
            
            # Zip log files & move zip file into backups folder & delete previous log files
            with ZipFile("../logs/backups/session.zip", 'w') as zip:
                for file in os.listdir("../logs/"):
                    if file.endswith(".log"):
                        zip.write(f"../logs/{file}")

# Trigger backup
backup_logs()


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
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": "../logs/master.log",
            "mode": "w",
            "encoding": "utf-8",
            "maxBytes": 6708864, # 64MB
            "backupCount": 10,
            "formatter": "custom"
        },
        "debug": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": "../logs/debug.log",
            "mode": "w",
            "encoding": "utf-8",
            "maxBytes": 6708864, # 64MB
            "backupCount": 10,
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