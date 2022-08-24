import mysql.connector
import json

# Check for company info
exec(open('read-info-from-db/GetCompanyInfo.py').read())

# db connection
db_connection_file = open('common/db-connection.json')
db_connection = json.load(db_connection_file)
proddb = mysql.connector.connect(
  host=db_connection['host'],
  user=db_connection['user'],
  password=db_connection['password'],
  database = db_connection['database']
)
if (proddb.is_connected()):
  print("\nConnection Successful", end=', ')
  print('Schema = ' + proddb.database)

getCursor = proddb.cursor()

companyID = str(input('Please enter company ID - '))

#inputs
print('1)  Enable Curbside')
print('2) Disable Curbside')
enableFlg = input('Please select Enable/Disable - ')#input
separator = "======================================================================================================================================================\n"
if (enableFlg=='1'):
  #enableFlg=True
  print('\n================================================================== Enable  Curbside ==================================================================\n')
elif (enableFlg=='2'):
  #enableFlg=False
  print('\n================================================================== Disable Curbside ==================================================================\n')
else:
  print('Incorrect input!')
  exit()

print('1)    Company-wide change')
print('2) Single Location change')
scope = input('Please select scope - ')#input

if scope=='1':
  companyID = str(input('Enter Company ID - '))#input
elif scope=='2':
  locationID = str(input('Enter Location ID - '))#input
else:
  print('Incorrect input!')
  exit()

#read configuration
if scope=='1':
  selectConfig = 'select * from configuration where company_id = '+companyID+' and code = "CURBSIDE_ENABLED" order by location_id;'
  selectLocation = 'select id from locations where company_loc_fk = '+companyID+' limit 1;'
  getCursor.execute(selectLocation)
  locationID = getCursor.fetchall()[0][0]

if scope=='2':
  selectConfig = 'select * from configuration where location_id = '+locationID+' and code like "%CURBSIDE%";'

getCursor.execute(selectConfig)
currentConfig = getCursor.fetchall() # Todo - Insert in case config not available
#exit()
#print(sfsdfaf)

if(scope == '1'): #Scope = Company
  #read feature_flags
  selectFeatureFlags = 'select * from feature_flags where company_id = (select company_loc_fk from locations where id = '+locationID+') order by updated_at;'
  getCursor.execute(selectFeatureFlags)
  currentFeatureFlags = getCursor.fetchall()
  print(separator+'Feature Flags ')
  for ctr in range(len(currentFeatureFlags)):
    print(str(ctr+1).rjust(2),end=") ")
    print(currentFeatureFlags[ctr][4])
  version = int(input('Please select the app version - '))-1 #input
  print('Version selected - '+currentFeatureFlags[version][4])

  
