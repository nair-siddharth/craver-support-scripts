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

  # Disable - Scope = Company
if((enableFlg=='2') and (scope=='1')):
  
  # Configuration Check
  updateConfig = 'update configuration SET value = "false" WHERE company_id = '+companyID+' and code = "CURBSIDE_ENABLED";'
  getCursor.execute(updateConfig)
  print('Config updated - '+str(getCursor.rowcount))
  proddb.commit()

  # Feature Flags Check
  for ctr in range (version,len(currentFeatureFlags)):
    featureFlags = currentFeatureFlags[ctr]
    #print(separator)
    print(str(ctr+1).rjust(2)+') '+featureFlags[4],end = " - ")
    featureFlagsJSON = json.loads(featureFlags[1])
    featureFlagsJSON["enableCurbsidePickup"] = False
    featureFlagsJSON["curbsidePickupToggleHide"] = True

    #if("enableCurbsidePickup" in featureFlagsJSON):
    #  featureFlagsJSON["enableCurbsidePickup"] = False
    #if("curbsidePickupToggleHide" in featureFlagsJSON):
    #  featureFlagsJSON["curbsidePickupToggleHide"] = True
    
    print(json.dumps(featureFlagsJSON),end = " - ")#,indent = 4,sort_keys=False))
    updateFeatureFlag = 'UPDATE feature_flags SET feature_flags = \''+json.dumps(featureFlagsJSON)+'\' WHERE (id = '+str(featureFlags[0])+');'
    getCursor.execute(updateFeatureFlag)
    print('Version updated - '+str(getCursor.rowcount))
    proddb.commit()


# Disable - Scope = Location
if((enableFlg=='2') and (scope=='2')):
  
  # Configuration Check
  updateConfig = 'update configuration SET value = "false" WHERE location_id = '+locationID+' and code = "CURBSIDE_ENABLED";'
  getCursor.execute(updateConfig)
  print('Config updated - '+str(getCursor.rowcount))
  proddb.commit()


# Enable - Scope = Company
if((enableFlg=='1') and (scope=='1')):
  
  # Configuration Check
  updateConfig = 'update configuration SET value = "true" WHERE company_id = '+companyID+' and code = "CURBSIDE_ENABLED";'
  getCursor.execute(updateConfig)
  print('Config updated - '+str(getCursor.rowcount))
  proddb.commit()

  # Update Configuration Instructions
  updateConfigInstructions = 'update configuration SET value = "'+input('Please enter curbside instructions here - ')+'" WHERE company_id = '+companyID
  updateConfigInstructions = updateConfigInstructions + ' and code = "CURBSIDE_INSTRUCTIONS";'
  getCursor.execute(updateConfigInstructions)
  print('Config updated - '+str(getCursor.rowcount))

  # Feature Flags Update
  for ctr in range (version,len(currentFeatureFlags),end = " - "):
    featureFlags = currentFeatureFlags[ctr]
    print(separator)
    print(str(ctr+1).rjust(2)+') '+featureFlags[4],end = " - ")
    featureFlagsJSON = json.loads(featureFlags[1])
    featureFlagsJSON["enableCurbsidePickup"] = True
    featureFlagsJSON["curbsidePickupToggleHide"] = False

    #if("enableCurbsidePickup" in featureFlagsJSON):
    #  featureFlagsJSON["enableCurbsidePickup"] = True
    #if("curbsidePickupToggleHide" in featureFlagsJSON):
    #  featureFlagsJSON["curbsidePickupToggleHide"] = False

    print(json.dumps(featureFlagsJSON),end = " - ")#,indent = 4,sort_keys=False))
    updateFeatureFlag = 'UPDATE feature_flags SET feature_flags = \''+json.dumps(featureFlagsJSON)+'\' WHERE (id = '+str(featureFlags[0])+');'
    getCursor.execute(updateFeatureFlag)
    print('Version updated - '+str(getCursor.rowcount))
    proddb.commit()


print('Enable')
# Enable - Scope = Location
if((enableFlg=='1') and (scope=='2')):
  
  if(len(currentConfig)==0):
    print()
    # insert curbside enable
    # insert curbside instructions
  else:
    # Configuration Update
    updateConfig = 'update configuration SET value = "true" WHERE location_id = '+locationID+' and code = "CURBSIDE_ENABLED";'
    getCursor.execute(updateConfig)
    print('Config updated - '+str(getCursor.rowcount))

    # Update Configuration Instructions
    updateConfigInstructions = 'update configuration SET value = "'+input('Please enter curbside instructions here - ')+'" WHERE location_id = '+locationID
    updateConfigInstructions = updateConfigInstructions + ' and code = "CURBSIDE_INSTRUCTIONS";'
    getCursor.execute(updateConfigInstructions)
    print('Config updated - '+str(getCursor.rowcount))
    proddb.commit()
