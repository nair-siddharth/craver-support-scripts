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

if(SMSInfo[0][0]==None):
	if(input('Feature not active, you want to activate it ? (Y/N) - ')=='y'):
		activateSMS = "UPDATE companies SET sms_auth_token = '5ce24bf211a446ca96ee860374ecbf9e', sms_account_sid = 'ACba7ac8553162a9f81013a9d7eb9003e8', sms_from_number = '+17782003334', sms_quota = '1000' WHERE (id = "+companyID+");"
		getCursor.execute(activateSMS)
		print(str(getCursor.rowcount) + ' rows affected')
		changeCount = getCursor.rowcount
	else:
		exit()

elif(SMSInfo[0][0]!=None):
	if(input('Feature active, you want to deactivate it ? (Y/N) - ')=='y'):
		deactivateSMS = "UPDATE companies SET sms_auth_token = null, sms_account_sid = null, sms_from_number = null, sms_quota = 0 WHERE (id = "+companyID+");"
		getCursor.execute(deactivateSMS)
		print(str(getCursor.rowcount) + ' rows affected')
		changeCount = getCursor.rowcount
	else:
		exit()


if(changeCount>0):
  if(input(str(changeCount)+' rows will be affected, continue? - ')=='y'):
    proddb.commit()
  else:
    print('Changes rolled back')

proddb.close()

if(not proddb.is_connected()):
  print("=====================================================================================================================================================")
  print("Successfully disconnected\n")
	
	