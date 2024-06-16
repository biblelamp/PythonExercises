###################################################### 
# Bulk deletion of access points OR funds in ELZA
from datetime import datetime
import requests
import json
import sys
import csv
import os

###################################################### 
# Before you start - carefully check everything again!
#

elzaPamatnic = 'https://elza.pamatnik-np.cz'
elzaSOAProdURL = 'https://elza.soapraha.cz'
elzaLocal = 'http://localhost:8080'

# current URL
elzaURL = elzaSOAProdURL

###################################################### 
# The first line of the csv file should contain the code of the type of deleted entities:
# - fund_id
# - access_point_id
# below, one per line, are the id of the deleted entities
# Example:
# fund_id
# 512
# 318
# ...
delete_mode = ''
delete_fund = 'fund_id'
delete_ap = 'access_point_id'


# read username and password from command line
if not sys.argv[1:]:
    print(f"Use: python {sys.argv[0]} <username> <password> [<path_file>]")
    sys.exit()
else:
    username = sys.argv[1]
    password = sys.argv[2]

# read path to file
if not sys.argv[3:]:
    #temp_dir = os.path.join('C:', os.sep, 'temp', 'la') #os.getcwd()
    temp_dir = os.getcwd()
else:
    temp_dir = sys.argv[3]

# read directory 'temp_dir' and try to find *.csv file
for file in os.listdir(temp_dir):
    if file.endswith(".csv"):
        file_csv = file
        break

if not 'file_csv' in locals():
    print('File *.csv not found')
    sys.exit()
else:
    print(os.path.join(temp_dir, file_csv))

# request POST to get JSESSIONID
res = requests.post(elzaURL + '/login', data={'username': username, 'password': password})
print('Read JSESSIONID: ', res.status_code, res.reason)
headers = res.headers
set_cookie = headers.get('Set-Cookie')
cookie = set_cookie[:set_cookie.index(';')]
print(cookie)

# process the csv file
with open(os.path.join(temp_dir, file_csv), newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        id = row[0]
        # set delete mode by name of column
        if not id.isnumeric():
            delete_mode = id
        else:
          # request DELETE to delete fund
          if delete_mode == delete_fund:
              res = requests.delete(elzaURL + '/api/arrangement/deleteFund/' + id,
                headers = {
                  'Content-Type': 'application/json',
                  'Cookie': cookie
                }
              )
              print(datetime.now(), 'fundId:', row[0], res.status_code, res.reason)
              f = open(os.path.join(temp_dir, 'deleted_funds.log'), 'a')
              f.write(str(datetime.now()) + ' ' + 'fundId: ' + str(row[0]) + ' ' + str(res.status_code) + ' ' + res.reason + '\n')
              f.close
          # request DELETE to delete access point
          if delete_mode == delete_ap:
              res = requests.delete(elzaURL + '/api/v1/accesspoints/' + id,
                headers = {
                  'Content-Type': 'application/json',
                  'Cookie': cookie
                }
              )
              print(datetime.now(), row[0], res.status_code, res.reason)
