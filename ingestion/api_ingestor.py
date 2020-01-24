import time
import datetime
import subprocess
from helpers import date_range

### URL + FILE
archive_domain = "https://data.gharchive.org/"
zip_file_ext = ".gz"
json_file_ext = ".json"

# DATA EXTRACT TO LOCAL


def api_to_local(filename):
    zip_filename = filename + zip_file_ext
    url = archive_domain + zip_filename
    # shell script
    subprocess.run(["wget", url])
    subprocess.run(["gzip", zip_filename, "-d"])


class Destination():
    def __init__(self, dest):
        self.dest = dest

    def move_to_dest(filename, datestring):
        print("Base Destination class:\nNo destination to move {} to".format(filename))


class EventsIngestor():
    def __init__(self, start_date, end_date, destination):
        self.start_date = start_date
        self.end_date = end_date
        self.destination = destination

    # API -> S3
    def hourly_events(self):
        # BY HOUR
        for singledate in date_range(self.start_date, self.end_date):
            for singlehour in range(24):
                # EXTRACT DATA
                datestring = (
                    (singledate + datetime.timedelta(hours=singlehour)).strftime("%Y-%m-%d-%-H"))
                filename = datestring + json_file_ext
                api_to_local(filename)
                # UPLOAD TO S3
                self.destination.move_to_dest(filename, datestring)
                # RM FROM LOCAL
                # shell script
                subprocess.run(["rm", filename])
                # LIMIT API ABUSE
                time.sleep(3)
