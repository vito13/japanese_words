import time
import datetime
from datetime import timedelta

#日期增加和减少
# now = datetime.datetime.now()
# print(type(now))
# datetime.datetime


# time.sleep(1)
# newdate = datetime.datetime.now() - now


# print(type(newdate))
# print(newdate.total_seconds())
from datetime import datetime
dt = datetime.today()  # Get timezone naive now
seconds = dt.timestamp()
print(dt)

# time.sleep(1)
# dt2 = datetime.today()  # Get timezone naive now

# print(seconds - seconds2)