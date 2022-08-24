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
#companyID='493'
