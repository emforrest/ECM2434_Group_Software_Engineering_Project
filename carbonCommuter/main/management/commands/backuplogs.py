import os
from zipfile import ZipFile

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Backs up the log files from the previous session.'

    def handle(self, *args, **options):
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
            if "session.zip" in os.listdir("../logs/backups/"):
                os.rename("../logs/backups/session.zip", "../logs/backups/session.1.zip")
            
            # Zip log files & move zip file into backups folder & delete previous log files
            with ZipFile("../logs/backups/session.zip", 'x') as zip:
                for file in os.listdir("../logs/"):
                    if ".log" in file:
                        zip.write(f"../logs/{file}", file)
                        os.remove(f"../logs/{file}")