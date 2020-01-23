#!/usr/bin/env python3
import sys
import time
import boto3
import datetime
import subprocess

### URL + FILE
archive_domain = "https://data.gharchive.org/"
zip_file_ext = ".gz"
json_file_ext = ".json"

### S3 CLIENT
s3_client = boto3.client('s3')

# source: https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
######

### DATA EXTRACT TO LOCAL
def api_to_local(filename):
	zip_filename = filename + zip_file_ext
	url = archive_domain + zip_filename
	## shell script
	subprocess.run(["wget", url])
	subprocess.run(["gzip", zip_filename, "-d"])


class EventsIngestor():
    def __init__(self, s3bucket, start_date, end_date):
        self.s3bucket = s3bucket
        self.start_date = start_date
        self.end_date = end_date

    ######## UPLOAD TO S3
    def upload_to_s3(self, filename, datestring):
        objectname = self.s3bucket + "-" + datestring
        ## run with nohup to print to nohup.out
        try:
            response = s3_client.upload_file(filename, self.s3bucket, objectname)
            print("trying {} @ {}".format(filename, time.time()))
        except Exception as e:
            print("error: {}".format(e))

    ### API -> S3
    def hourly_events(self):
    	### BY HOUR
        for singledate in daterange(self.start_date, self.end_date):
            for singlehour in range(24):
                ###### EXTRACT DATA
                datestring = ((singledate + datetime.timedelta(hours=singlehour)).strftime("%Y-%m-%d-%-H"))
                filename = datestring + json_file_ext
                api_to_local(filename)
                ######## UPLOAD TO S3
                self.upload_to_s3(filename, datestring)
                ### RM FROM LOCAL
                ## shell script
                subprocess.run(["rm", filename])

                ## LIMIT API ABUSE
                time.sleep(3)


if __name__ == "__main__":
    s3bucket = "git-events" if len(sys.argv) == 1 else sys.argv[1]
	### DATE RANGE
    if len(sys.argv) >= 5:
        start_date = datetime.datetime(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), 0)
        if len(sys.argv) >= 8:
            end_date = datetime.datetime(int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), 0)
        else:
            end_date = datetime.datetime(2020,1,19,0)
    else:
        start_date = datetime.datetime(2012,1,1,0)

    ### DEFINE INGESTOR
    ## run with nohup to print to nohup.out
    print("S3 Bucket: {}\nStart Date: {}\nEnd Date: {}".format(s3bucket, start_date, end_date))
    Ingestor = EventsIngestor(s3bucket, start_date, end_date)

	### RUN
    try:
        Ingestor.hourly_events()
    except KeyboardInterrupt:
        None
    sys.exit(0)
