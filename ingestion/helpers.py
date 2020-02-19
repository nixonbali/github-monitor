import datetime

# source: https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def date_range(start_date, end_date):
    """Yields Daily Incrementing Dates for Input Time Range"""
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def date_reader(inputs):
    """Converts Command Line Input Date Parameters to datetime"""
    start_date = datetime.datetime(2012,1,1,0)
    end_date = datetime.datetime(2020,1,19,0)
    if len(inputs) >= 4:
        start_date = datetime.datetime(int(inputs[0]), int(inputs[1]), int(inputs[2]), int(inputs[3]))
    if len(inputs) >= 8:
        end_date = datetime.datetime(int(inputs[4]), int(inputs[5]), int(inputs[6]), int(inputs[7]))
    return(start_date, end_date)
