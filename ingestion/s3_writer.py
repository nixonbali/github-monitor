#!/usr/bin/env python3
from api_ingestor import Destination, EventsIngestor
from helpers import date_reader
import boto3
import sys

### S3 CLIENT
s3_client = boto3.client('s3')

class Bucket(Destination):
    # self.dest is s3bucket
    ######## UPLOAD TO S3
    def move_to_dest(self, filename, datestring):
        objectname = self.dest + "-" + datestring
        ## run with nohup to print to nohup.out
        try:
            response = s3_client.upload_file(filename, self.dest, objectname)
            print("trying {} @ {}".format(filename, time.time()))
        except Exception as e:
            print("error: {}".format(e))

if __name__ == "__main__":
    s3bucket_name = "git-events" if len(sys.argv) == 1 else sys.argv[1]
    start_date, end_date = date_reader(sys.argv[2:])
    ## run with nohup to print to nohup.out
    print("S3 Bucket: {}\nStart Date: {}\nEnd Date: {}".format(s3bucket_name, start_date, end_date))

    ## Define destination and ingestion objects
    S3Bucket = Bucket(s3bucket_name)
    Ingestor = EventsIngestor(start_date, end_date, S3Bucket)

	### RUN
	try:
		Ingestor.hourly_events()
	except KeyboardInterrupt:
		None
	sys.exit(0)
