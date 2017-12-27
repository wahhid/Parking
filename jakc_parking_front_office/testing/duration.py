
from datetime import datetime
from dateutil.relativedelta import relativedelta


diff = relativedelta(datetime.strptime('2015-12-24 05:00:00','%Y-%m-%d %H:%M:%S'),datetime.strptime('2015-11-24 04:00:00','%Y-%m-%d %H:%M:%S') )
print diff