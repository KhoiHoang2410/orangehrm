import requests
import datetime
import random

def apply_leave(emp_number, fromDate, toDate):
  cookies = {
    '_orangehrm': 'd1f8a1803201b0bccacfb1493b30ee88',
  }
  json_data = {
    'leaveTypeId': 1,
    'fromDate': fromDate,
    'toDate': toDate,
    'comment': None,
    'empNumber': emp_number,
  }
  return requests.post('http://localhost:8200/web/index.php/api/v2/leave/employees/leave-requests', cookies=cookies, json=json_data)

date_format = '%Y-%m-%d'
from_date = datetime.datetime.strptime('2022-05-01', date_format)

for i in range(7552, 20002):
  leave_day = random.randint(1, 25)
  to_date = from_date + datetime.timedelta(days=leave_day)

  response = apply_leave(i, from_date.strftime(date_format), to_date.strftime(date_format))

  print(response.status_code)
  