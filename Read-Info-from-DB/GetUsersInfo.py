import mysql.connector
import requests
import time
import csv
import json

# inputs
# Check for company info
# exec(open('Read-Info-from-DB/GetCompanyInfo.py').read())
# db connection
db_connection_file = open('/Users/siddharthnair/Documents/GitHub/craver-support-scripts/Read-Info-from-DB/db-connection.json')
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
selectUsers = 'select id, name,email,telephone,points,balance,giftcard_id from users where company_fk='+companyID+' limit 20;'
getCursor.execute(selectUsers)
users = getCursor.fetchall()
ct = 0

# open csv file
f = open('UsersList.csv', 'w')
writer = csv.writer(f)
rowArr = ['ID', 'Name', 'Email', 'Phone', 'Points',
    'Gift Card Balance', 'Wallet Balance']
writer.writerow(rowArr)
urlGiftCardBalance = db_connection["gift-card-balance-API"]
api_token = db_connection["gift-card-api-token"]
for user in users:
  giftCard = user[6]
  ct = ct+1

  if (giftCard):
    header = {"Authorization": "Bearer "+api_token}
    giftCard = requests.get(urlGiftCardBalance+giftCard, headers=header)
    try:
      rowArr = [user[0],user[1],user[2],user[3],user[4],user[5],giftCard.json()['balance']]
    except:
      rowArr = [user[0],user[1],user[2],user[3],user[4],user[5],'0']
  else:
    rowArr = [user[0],user[1],user[2],user[3],user[4],user[5],'0']
  writer.writerow(rowArr)
  time.sleep(.1)

f.close()

# close connection
proddb.close()
if(not proddb.is_connected()):
  print("=====================================================================================================================================================")
  print("Successfully disconnected\n")



  

