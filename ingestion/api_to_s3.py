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

# source:
# https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
######

### DATA EXTRACT TO LOCAL
def api_to_local(filename):
	zip_filename = filename + zip_file_ext
	url = archive_domain + zip_filename
	## shell script
	subprocess.run(["wget", url])
	subprocess.run(["gzip", zip_filename, "-d"])



### API -> S3
def hourly_events(start_date, end_date, s3bucket="git-events", logging=True):
	### INITIATE LOG
	if logging:
		starttime = prevtime = time.time()
		with open("logs/gh-events.log", "w") as logfile:
			logfile.write("Time\t\t\tTime Since Last\t\tTime Since Start\t\t\t\n")

	### BY HOUR
	for singledate in daterange(start_date, end_date):
		for singlehour in range(24):

			###### EXTRACT DATA
			datestring = ((singledate + datetime.timedelta(hours=singlehour)).strftime("%Y-%m-%d-%-H"))
			filename = datestring + json_file_ext
			api_to_local(filename)

			######## UPLOAD TO S3
			object_name = "git-events-" + datestring
			try:
				response = s3_client.upload_file(filename, s3bucket, object_name)
				print("trying {}".format(time.time()))
			except Exception:
				print("error: {}".format(e))

			### RM FROM LOCAL
			## shell script
			subprocess.run(["rm", filename])

			time.sleep(3)

			####### LOG TIME
			with open("logs/gh-events.log", "a+") as logfile:
				t = time.time()
				logfile.write("{}\t{}\t{}\n".format(t, t-prevtime, t-starttime))
				prev_time = t

if __name__ == "__main__":
	### DATE RANGE
	if len(sys.argv) == 1:
		start_date = datetime.datetime(2012,1,1,0)
		end_date = datetime.datetime(2020,1,19,0)
	elif len(sys.argv) == 4:
		start_date = datetime.datetime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), 0)
		end_date = datetime.datetime(2020,1,19,0)
	elif len(sys.argv) == 7:
		start_date = datetime.datetime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), 0)
		end_date = datetime.datetime(int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), 0)
	else:
		print("Invalid Arguments: Must be None, 3, or 6.\nstart_date: YYYY M D\nend_date: YYYY M D")
		sys.exit(0)

	### RUN
	try:
		hourly_events(start_date, end_date, s3bucket="git-events")
	except KeyboardInterrupt:
		None
	sys.exit(0)
