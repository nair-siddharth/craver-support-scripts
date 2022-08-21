import mysql.connector
import requests
import time
import csv

#inputs
# Check for company info
#exec(open('Read-Info-from-DB/GetCompanyInfo.py').read())
#db connection
proddb = mysql.connector.connect(
  host=input('Please enter host IP - '),
  user=input('Please enter user name - '),
  password=input('Please enter your password - '),
  database = input('Please enter the schema name - ')
)

if(proddb.is_connected()):
  print("\nConnection Successful", end = ', ')
  print('Schema = ' + proddb.database)

getCursor = proddb.cursor()

companyID = input("\nPlease enter company ID - ")
selectUsers = 'select id, name,email,telephone,points,balance,giftcard_id from users where company_fk='+companyID+';'
getCursor.execute(selectUsers)
users = getCursor.fetchall()
ct=0

#open 
f = open('UsersList.csv', 'w')
writer = csv.writer(f)
rowArr  = ['ID','Name','Email','Phone','Points', 'Gift Card Balance', 'Wallet Balance']
writer.writerow(rowArr)
urlGiftCardBalance = 'Enter Gift Cards API Endpoint (please check with devs for more info) - '
api_token = 'Enter api_token (please check with devs for more info) - '
for user in users:
	giftCard = user[6]
	ct=ct+1

	if(giftCard):
		urlGiftCardBalance = urlGiftCardBalance+giftCard
		#print(urlGiftCardBalance)
		
		header = {"Authorization":"Bearer "+api_token}
		giftCard = requests.get(urlGiftCardBalance,headers = header)
		rowArr = [user[0],user[1],user[2],user[3],user[4],user[5],giftCard.json()['balance']]
		time.sleep(.01)

	else:
		rowArr = [user[0],user[1],user[2],user[3],user[4],user[5],'0']
	writer.writerow(rowArr)

f.close()

#close connection
proddb.close()
if(not proddb.is_connected()):
  print("=====================================================================================================================================================")
  print("Successfully disconnected\n")



	

