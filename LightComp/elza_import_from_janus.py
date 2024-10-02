###############################################################################
# Bulk import of data from Janus to Elza
import os
import csv
import requests
import sys
import zipfile
from datetime import datetime
from bs4 import BeautifulSoup # pip3 install bs4
from requests_toolbelt.multipart.encoder import MultipartEncoder # pip3 install requests_toolbelt
import pandas as pd # pip install pandas

###############################################################################
# GOOGLE SHEETS constants
SHEET_ID = '1EyCJdUwAPmirw8YPs1Gu710DHwBaPPVAzikB-wxwk7Q'
CENTR_DB_TAB = '221011-databaze' # central database
BENESOV_TAB =        'BE'
KOLIN_TAB =          'KO'
KUTNA_HORA_TAB =     'KH'
KLADNO_TAB =         'KL'
MLADA_BOLESLAV_TAB = 'MB'
MELNIK_TAB =         'ME'
NYMBURK_TAB =        'NY'
PRIBRAM_TAB =        'PB'
RAKOVNIK_TAB =       'RA'
PRAHA_VYCHOD_TAB =   'PV'
PRAHA_ZAPAD_TAB =    'PZ'

## current tab of sheet
TAB_NAME = PRAHA_ZAPAD_TAB

# full address of table
sheet_url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={TAB_NAME}'

###############################################################################
# LA PNP constants

#elzaURL = 'https://elza.pamatnik-np.cz' # 'https://elza-test.pamatnik-np.cz'
#convertURL = 'https://elza-convert.pamatnik-np.cz'
#institution_code = 630000020
#lapnp_t1 = 'LAPNP_t1'
#lapnp_t1_digit = 'LAPNP_t1_digit'
#scope_id = '3'

###############################################################################
# SOA Praha constants
elzaSOATestURL = 'https://elza-test.soapraha.cz'
elzaSOAProdURL = 'https://elza.soapraha.cz'

convertSOAPrahaURL = 'https://elza-test.soapraha.cz'

# cities codes
benesov_code        = 221201010
beroun_code         = 221202010
kladno_code         = 221203010
kolin_code          = 221204010
kutna_hora_code     = 221205010
melnik_code         = 221206010
mlada_boleslav_code = 221207010
nymburk_code        = 221208010
pribram_code        = 221211010
rakovnik_code       = 221212010
praha_vychod_code   = 221209010
praha_zapad_code    = 221210010
praha_zapad_code_2  = 221202010
centrala_code       = 211000010

# yaml files
soa_praha_t1          = 'SOAPraha_t1' # central database
soa_benesov_t1        = 'SOABenesov_t1'
soa_nymburk_t1        = 'SOANymburk_t1'
soa_kutna_hora_t1     = 'SOAKutnaHora_t1'
soa_kladno_t1         = 'SOAKladno_t1'
soa_kolin_t1          = 'SOAKolin_t1'
soa_mlada_boleslav_t1 = 'SOAMladaBoleslav_t1'
soa_melnik_t1         = 'SOAMelnik_t1'
soa_pribram_t1        = 'SOAPribram_t1'
soa_rakovnik_t1       = 'SOARakovnik_t1'
soa_praha_vychod_t1   = 'SOAPrahaVychod_t1'
soa_praha_zapad_t1    = 'SOAPrahaZapad_t1'

soa_scope_id = '84'

###############################################################################
# INIT common variable
###############################################################################
elzaURL = elzaSOAProdURL	 # SOA test/prod
convertURL = convertSOAPrahaURL	 # convertor SOA
institution_code = praha_zapad_code_2    # kolin
yaml_file = soa_praha_zapad_t1         # yaml file
scope_id = soa_scope_id	         # scope

# common constants
processJanus = "/processJanus"
import_xml = 'import.xml'
name_postfix = ' (import Janus)'
protokol_txt = 'protokol.txt'
ok = 'ok'
error = 'error'
error_list_log = 'error_list.log'
max_error_count = 50 # maximum permissible error rate

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

#if not 'file_csv' in locals():
#    print('File *.csv not found')
#    sys.exit()

print('#########################################################')
print('#   Check all parameters carefully before continuing!   #')
print('#########################################################')
#print('CsvFile: ', os.path.join(temp_dir, file_csv))
print('SheetURL:', sheet_url)
print('ElzaURL:', elzaURL)
print('ConvertURL:', convertURL)
print('institution_code:', institution_code)
print('yaml_file:', yaml_file)
print('scope_id:', scope_id)

yes_no = input('Continue: [Y/n]:')
if yes_no != 'Y' and yes_no != 'y':
    sys.exit()

only_test = input('Only test: [N/y]:')

# control of consistency of the yaml file and the google sheet tab
if (TAB_NAME == CENTR_DB_TAB and yaml_file != soa_praha_t1) or (yaml_file == soa_praha_t1 and TAB_NAME != CENTR_DB_TAB):
    print('Error:', yaml_file, 'is inconsistent with', TAB_NAME)
    sys.exit()

# process the google sheet
#with open(os.path.join(temp_dir, file_csv), newline='') as csvfile:
#reader = csv.reader(csvfile, delimiter=',', quotechar='"')
#row_count = 0
df = pd.read_csv(sheet_url)
for index, row in df.iterrows():
    #row_count += 1
    #row_nad = int(row[0])
    #if index in range(1, 1260): # import SOA

    #if index in [502, 503, 504]:
    #    print(row[0], row[3], row[4], row[6])

    # filter by content of column "D"
    if row[3] != institution_code:
        continue

    # filter by content of column "E"
    if row[4] != 'K převodu': # 'K převodu','Převedeno v testu','Chyba'
        continue

    # filter by content of column "G" (only on central database)
    if (TAB_NAME == CENTR_DB_TAB):
        if row[6] != 'AB':
            continue

    # filter by fund number (385)
    #if (int(row[2]) != 385):
    #  continue

    # data from table's row
    fund_number = int(row[2])
    fund_name = row[1] + name_postfix
    db_name = row[0]
    file_dir = os.path.join(temp_dir, db_name)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # length of the name cannot exceed 50 characters
    if len(fund_name) > 50:
        fund_name = db_name + name_postfix

    # only test or real processing?
    print(index + 2, row[0], row[1], int(row[2]), int(row[3]), row[4], (row[6] if len(row) > 6 else TAB_NAME))
    if only_test == 'Y' or only_test == 'y':
      continue

    # use different templates, by content of column "F"
    #if row[5] == 'ano':
    #    yaml_file = lapnp_t1_digit
    #else:
    #    yaml_file = lapnp_t1

    # request POST to get url
    res = requests.post(convertURL + processJanus,
        data = {
            'institutionCode': institution_code,
            'fundName': fund_name,
            'fundNumber': fund_number,
            'dbName': db_name,
            'yamlFile': yaml_file
        })
    print('POST:', res.status_code, res.reason)
    
    # print(res.text)
    parserHtml = BeautifulSoup(res.text, features="html.parser")
    resultHref = parserHtml.body.find('a', attrs={'class' : 'btn btn-primary'})
    if resultHref is None:
        print('ERROR: resultHref not found.')
        f = open(os.path.join(file_dir, error), 'w')
        f.write(res.text)
        f.close()
        # error logging
        f = open(os.path.join(temp_dir, error_list_log), 'a')
        f.write(str(datetime.now()) + ' ' + db_name + '\n')
        f.close
        continue
    else:
        resultURL = resultHref.get('href')

    file_name_uuid = resultURL[8:]
    #print(resultURL)
    print('UUID:', file_name_uuid)

    # request GET to get data and save to file
    res = requests.get(convertURL + resultURL)
    print('GET:', res.status_code, res.reason)
    content_data = res.content
    file_name = os.path.join(file_dir, str(fund_number) + '.zip')
    f = open(file_name, "wb")
    f.write(content_data)
    f.close()
    #unzip file
    zip_ref = zipfile.ZipFile(file_name)
    zip_ref.extractall(file_dir)
    zip_ref.close()
    #print(content_data)

    # count lines in protokol.txt
    protokol_file = os.path.join(file_dir, protokol_txt)
    f = open(protokol_file, "r")
    line_count = len(f.readlines())
    f.close()
    f = open('protokol_lines.csv', 'a')
    f.write(db_name + "," + str(line_count) + "\n")
    f.close()
    print('ERROR:', str(line_count))

    # if count of errors is greater than max_error_count
    if line_count > max_error_count:
        f = open(os.path.join(temp_dir, error_list_log), 'a')
        f.write(str(datetime.now()) + ' ' + db_name + ' error:' + str(line_count) + '\n')
        f.close
        # if this is a test, the processing must be continued
        if elzaURL != elzaSOATestURL:
            continue

    # request POST to get JSESSIONID
    res = requests.post(elzaURL + '/login', data={'username': username, 'password': password})
    print('POST:', res.status_code, res.reason)
    headers = res.headers
    set_cookie = headers.get('Set-Cookie')
    cookie = set_cookie[:set_cookie.index(';')]
    print(cookie)

    # request POST to import data
    file_contents = open(os.path.join(file_dir, import_xml), 'rb').read()
    mp_encoder = MultipartEncoder(
        fields = {
            'scopeId': scope_id,
            'xmlFile': (import_xml, file_contents, 'text/plain')
        }
    )
    res = requests.post(elzaURL + '/api/import/import',
        data = mp_encoder,
        headers = {
            'Content-Type': mp_encoder.content_type,
            'Cookie': cookie
        }
    )
    print('POST:', res.status_code, res.reason)
    #print(res.text)
    if res.status_code == 200:
        f = open(os.path.join(file_dir, ok), 'w')
        f.close
    else:
        f = open(os.path.join(file_dir, error), 'w')
        f.write(cookie + "\n" + str(res.status_code) + "\n" + res.text)
        f.close()
        # error logging
        f = open(os.path.join(temp_dir, error_list_log), 'a')
        f.write(str(datetime.now()) + ' ' + db_name + '\n')
        f.close