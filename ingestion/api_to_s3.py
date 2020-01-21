#!/usr/bin/env python
import sys
import time
import boto3
import datetime
import subprocess

### URL + FILE
archive_domain = "https://data.gharchive.org/"
zip_file_ext = ".gz"
json_file_ext = ".json"

### S3 BUCKET
s3_client = boto3.client('s3')
s3bucket = "git-events"

### LOGGING
starttime = prevtime = time.time()
with open("logs/gh-events.log", "w") as logfile:
	logfile.write("Time\t\t\tTime Since Last\t\tTime Since Start\t\t\t")

### DATE RANGE
start_date = datetime.datetime(2012,1,1,0)
end_date = datetime.datetime(2020,1,19,0)
# source:
# https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
######


try:
	### BY HOUR
	for singledate in daterange(start_date, end_date):
		for singlehour in range(24):

			###### EXTRACT DATA
			datestring = ((singledate + datetime.timedelta(hours=singlehour)).strftime("%Y-%m-%d-%-H"))
			filename = datestring + json_file_ext
			zip_filename = filename + zip_file_ext
			url = archive_domain + zip_filename

			## shell script
			subprocess.run(["wget", url])
			subprocess.run(["gzip", zip_filename, "-d"])

			######## UPLOAD TO S3
			object_name = "git-events-" + datestring
			try:
				response = s3_client.upload_file(filename, s3bucket, object_name)
				print("trying {}".format(time.time()))
			except Exception:
				print("error: {}".format(e))

			## shell script
			subprocess.run(["rm", filename])

			time.sleep(3)

			####### LOG TIME
			with open("logs/gh-events.log", "a+") as logfile:
				t = time.time()
				logfile.write("{}\t{}\t{}".format(t, t-prevtime, t-starttime))
				prev_time = t




except KeyboardInterrupt:
	None

sys.exit(0)
