####################################################################
# Processing a table to eliminate of duplication of entities in ELZA
import os
import sys
import csv
import requests
import json
from pathlib import Path

# elza url & request
elza_url = 'https://elza.pamatnik-np.cz' #'http://localhost:3000'
request_value = '/api/v1/accesspoint/'

# read username and password from command line
if not sys.argv[1:]:
    print(f"Use: python {sys.argv[0]} <username> <password> [<path_file>]")
    sys.exit()
else:
    username = sys.argv[1]
    password = sys.argv[2]

# read path to file
if not sys.argv[3:]:
    temp_dir = os.getcwd()
else:
    temp_dir = sys.argv[3]

# read directory 'temp_dir' and try to find first *.csv file
for file in os.listdir(temp_dir):
    if file.endswith(".csv"):
        file_csv = file
        break

if not 'file_csv' in locals():
    print('File *.csv not found')
    sys.exit()

# create log file
file_log = os.path.join(temp_dir, Path(sys.argv[0]).stem + '.log')

# reading csv file
with open(file_csv, mode = 'r') as file:

    # request POST to get JSESSIONID
    res = requests.post(elza_url + '/login', data={'username': username, 'password': password})
    print('POST:', res.status_code, res.reason)
    headers = res.headers
    set_cookie = headers.get('Set-Cookie')
    cookie = set_cookie[:set_cookie.index(';')]
    print(cookie)

    # creating a csv reader object
    csv_reader = csv.reader(file, delimiter=';')

    # extracting field names through first row
    fields = next(csv_reader)
    print(fields)

    # only 1st row processed
    only_1st_row = False

    # extracting each data row one by one
    for row in csv_reader:
        id = row[0]
        replaced_by = row[3]
        print(id, 'replace by', replaced_by)

        # prepare data
        payload = {'replacedBy': replaced_by, 'replaceType': 'SIMPLE'}

        # request DELETE to replace access_point
        res = requests.delete(elza_url + request_value + id,
            data = json.dumps(payload),
            headers = {'Content-Type': 'application/json',
                       'Cookie': cookie}
        )
        print('DELETE:', res.status_code, res.reason)

        # write to log file
        log = open(file_log, 'a')
        log.write(" ".join([id, 'replace by', replaced_by, '-', str(res.status_code), res.reason, '\n']))
        log.close()

        # only 1st row processed or all rows
        if only_1st_row:
            break
