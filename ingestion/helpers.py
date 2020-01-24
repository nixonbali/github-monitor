import datetime

# source: https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
######

### DATE RANGE
def date_reader(inputs):
    if len(inputs) >= 3:
        start_date = datetime.datetime(int(inputs[0]), int(inputs[1]), int(inputs[2]), 0)
        if len(inputs) >= 6:
            end_date = datetime.datetime(int(inputs[3]), int(inputs[4]), int(inputs[5]), 0)
        else:
            end_date = datetime.datetime(2020,1,19,0)
    else:
        start_date = datetime.datetime(2012,1,1,0)
    return(start_date, end_date)
