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

print('====================================================================== Close a Company ======================================================================')
changeCount = 0
companyID = str(input('Enter company ID - '))

deleteLocations = "UPDATE locations SET is_deleted = b'1' where company_loc_fk="+companyID+";"
getCursor.execute(deleteLocations)
changeCount = changeCount + getCursor.rowcount

disableAdmins = "UPDATE admins SET is_disabled = b'1' WHERE email not like '%@admin.com%' and company_fk="+companyID+";"
getCursor.execute(disableAdmins)
changeCount = changeCount + getCursor.rowcount


if(input(str(changeCount) + ' rows affected, are you sure you want to mark the company closed? - ')=='y'):
  proddb.commit()
else:
  print(str(changeCount) + ' changed rolled back')
  exit()

print("\n=====================================================================================================================================================\n")

print('If you wish, you can check if the changes were done correctly')
exec(open('read-info-from-db/GetCompanyInfo.py').read())
#close db connection
proddb.close()
if(not proddb.is_connected()):
  print("=====================================================================================================================================================")
  print("Successfully disconnected\n")


