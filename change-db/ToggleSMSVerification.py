import mysql.connector
# Check for company info
exec(open('GetAllCompanyInfo.py').read())
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
companyID = input("\nPlease enter company ID - ")

print('====================================================================== SMS Verification ======================================================================')
companyID = str(input('Enter Company ID - '))
changeCount = 0

selectSMSInfo = 'select sms_auth_token,sms_account_sid,sms_from_number,sms_quota from companies where id='+companyID+';'
getCursor.execute(selectSMSInfo)
SMSInfo = getCursor.fetchall()

