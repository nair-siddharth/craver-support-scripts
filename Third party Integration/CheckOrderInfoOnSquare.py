import mysql.connector
import json
import requests
import sys

def first100_Orders(extLocationID,externalOrderID,bearerToken):
  #Batch retrieve - Max 100 orders returned
  url = "https://connect.squareup.com/v2/orders/batch-retrieve"
  #data = {"location_id":"LWTYAJH3H1T0D","order_ids":["cNSYwsVdOUvchugBV4ye1O5Ds7dZY","YJdETKqEVSB0gP70OxuQQ4exHocZY"]}
  data = {"location_id":extLocationID,"order_ids":externalOrderID}
  header = {"Authorization": bearerToken}
  try:
    postRequest = requests.post(url,headers=header,json=data)
    jsonSquareOrders = postRequest.json()
  except:
    print(postRequest.text)
    proddb.close()
    sys.exit()

  countMismatchStatus=0
  countMismatchTotal=0

  try:
    print(len(jsonSquareOrders["orders"]))
  except:
    print(len(externalOrderID))
    print(jsonSquareOrders)
    input()

  for ctrSq in range(len(jsonSquareOrders["orders"])):
    #print(str(ctrSq).ljust(4)+". "+ jsonSquareOrders["orders"][ctrSq]["id"]+" Square <---------> Craver "+externalOrderID[ctrSq])
    print(str(selectedOrders[ctrSq][0]).ljust(10),end="")
    print(jsonSquareOrders["orders"][ctrSq]["updated_at"].ljust(25),end="")
    print(jsonSquareOrders["orders"][ctrSq]["state"].ljust(15),end="")
    print(selectedOrders[ctrSq][1].ljust(15),end="")
    print(jsonSquareOrders["orders"][ctrSq]["id"].ljust(40),end="")
    print(str(selectedOrders[ctrSq][5]).ljust(10),end="")
    print(str(jsonSquareOrders["orders"][ctrSq]["total_money"]["amount"]/100).ljust(10),end="\n")

  return (ctrSq+1)
#### End of Function

def GetMoreThan100_Orders_OneByOne(externalOrderID,url,header,diffOnly):

  countOrders = 0
  diffCount = 0
  for ctrOrder in range(len(externalOrderID)):
    getRequest = requests.get(url+externalOrderID[ctrOrder],headers=header)
    countOrders+=1
    jsonSquareOrder = getRequest.json()

    if( (diffOnly == 'y' or diffOnly == 'Y') and (
      not(jsonSquareOrder["order"]["state"] == selectedOrders[ctrOrder][1]) 
      or 
      not(round(selectedOrders[ctrOrder][5],1)==round(jsonSquareOrder["order"]["total_money"]["amount"]/100),1) ) ) :
      
      diffCount+=1
      print(str(selectedOrders[ctrOrder][0]).ljust(10),end="")
      print(jsonSquareOrder["order"]["updated_at"].ljust(25),end="")
      print(jsonSquareOrder["order"]["state"].ljust(15),end="")
      print(selectedOrders[ctrOrder][1].ljust(15),end="")
      print(jsonSquareOrder["order"]["id"].ljust(40),end="")
      print(str(round(selectedOrders[ctrOrder][5],2)).ljust(10),end="")
      print(str(round(jsonSquareOrder["order"]["total_money"]["amount"]/100,2)).ljust(10),end="\n")        

    if(diffOnly == 'n' or diffOnly =='N'):
      print(str(selectedOrders[ctrOrder][0]).ljust(10),end="")
      print(jsonSquareOrder["order"]["updated_at"].ljust(25),end="")
      print(jsonSquareOrder["order"]["state"].ljust(15),end="")
      print(selectedOrders[ctrOrder][1].ljust(15),end="")
      print(jsonSquareOrder["order"]["id"].ljust(40),end="")
      print(str(selectedOrders[ctrOrder][5]).ljust(10),end="")
      print(str(jsonSquareOrder["order"]["total_money"]["amount"]/100).ljust(10),end="\n")  

    
  if(diffOnly == 'y' or diffOnly == 'Y'):
    print('Difference Count = '+ str(diffCount),end = " :: ")
  return (countOrders)
#### End of function

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

locationID = input("Please enter location ID below - ")
diffOnly = 'n'
val=None

if(int(locationID)<2000):
  startDate = input("Please start date of orders (YYYY-MM-DD) - ")
  endDate = input("Please end date of orders (YYYY-MM-DD) - ")
  diffOnly = input('Print only mismatched Status? (Y/N) - ')
try:
  val = (locationID,startDate,endDate)
except:
  val = tuple([locationID])
  print(val)

#Order Info
selectOrdersFromCraver = "select id,orderStatus,deliveryOption,external_order_id,external_fulfillment_id,calculated_total from orders where location_fk=%s and placed_at >=%s and placed_at<=%s order by updated_at desc;"

if(int(locationID)>2000):
  selectOrdersFromCraver = "select id,orderStatus,deliveryOption,external_order_id,external_fulfillment_id,calculated_total from orders where id=%s;"
  

getCursor.execute(selectOrdersFromCraver,val)
selectedOrders = getCursor.fetchall()
try:
  selectedOrders[0]
except:
  print("No Craver orders found")
  proddb.close()
  sys.exit()
if(len(selectedOrders)>10):
  if( input(str(len(selectedOrders))+' orders found! Do you want to continue(Y/N)? - ') =='n' ):
    exit()

externalOrderID = []

for ctr in range(len(selectedOrders)):
  externalOrderID.append(selectedOrders[ctr][3])

#Square API Header + Data from Craver
#Auth Token
selectAuthInfo = "select pos_integration_credentials from companies where id = (select distinct company_loc_fk from locations where id="+str(locationID)+")"

if(int(locationID)>2000):
  selectAuthInfo = "select pos_integration_credentials from companies where id = (select company_ord_fk from orders where id = "+str(locationID)+");"

getCursor.execute(selectAuthInfo)
bearerToken = getCursor.fetchall()[0][0]
bearerToken="Bearer "+bearerToken[ bearerToken.find(":") +1: ]

#Square Location ID
selectLocationExtID = "select square_id from square_servers where id = (select square_server_id from locations where id="+str(locationID)+")"
if(int(locationID)>2000):
  selectLocationExtID = "select square_id from square_servers where id = (select square_server_id from locations where id = (select location_fk from orders where id="+str(locationID)+"));"

getCursor.execute(selectLocationExtID)
extLocationID = getCursor.fetchall()[0][0]

