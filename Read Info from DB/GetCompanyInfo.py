import mysql.connector

#inputs
#DB connection
proddb = mysql.connector.connect(
  host=input('Please enter host IP - '),
  user=input('Please enter user name - '),
  password=input('Please enter your password - '),
  database = input('Please enter the schema name - ')
)
#print(proddb.database)
if(proddb.is_connected()):
  print("\nConnection Successful")

getCursor = proddb.cursor()

companyName = input("Please enter company name - ")
if(companyName == ''):
  print('No search string entered; please try again')
  exit()
verboseFlg = 'y'


#outputs
#Read Company Info
selectCompanies = "select * from companies where name like \"%"+companyName+"%\";"

getCursor.execute(selectCompanies)
companies = getCursor.fetchall()

#Confirm if too many matching results found
if(len(companies)>3):
  checkResultCt = input(str(len(companies))+" results found! Do you want to continue? (Y/N) - ")
  if(checkResultCt!="Y" and checkResultCt!="y"):
    exit()
  verboseFlg = input("Would like to see Detailed info (Y/N)? - ")#Do you want to see basic or detaild info?

ID = []
Name = []
APIToken = []
POSIntegration=[]
PaymentIntegration=[]
LoyaltyIntegration=[]
DeliveryIntegration=[]
PaymentIntegrationCredentials=[]
POSIntegrationCredentials=[]
LoyaltyProgramID=[]
LoyaltyProgramIntegrationID=[]
PaymentCredentialID=[]
SquareMerchantID=[]


# read from companies
for ctr in range(len(companies)):
  ID.append(companies[ctr][0])
  Name.append(companies[ctr][1])
  APIToken.append(companies[ctr][2])
  POSIntegration.append(companies[ctr][3])
  PaymentIntegration .append(companies[ctr][4])
  DeliveryIntegration.append(companies[ctr][27])
  LoyaltyIntegration.append(companies[ctr][5])
  PaymentIntegrationCredentials.append(companies[ctr][7])
  POSIntegrationCredentials.append(companies[ctr][8])
  LoyaltyProgramID.append(companies[ctr][39])
  LoyaltyProgramIntegrationID.append(companies[ctr][40])
  PaymentCredentialID.append(companies[ctr][41])
  SquareMerchantID.append(companies[ctr][50])


for ctr in range(len(companies)):
  print("=====================================================================================================================================================")
  print("ID : ".ljust(30)+str(ID[ctr]))
  print("Name : ".ljust(30)+str(Name[ctr]))
  print("API Token : ".ljust(30)+str(APIToken  [ctr]))
  print("POS Integration : ".ljust(30)+str(POSIntegration[ctr]))
  print("Payments through ".ljust(30)+str(PaymentIntegration[ctr]))
  print("Deliveries handled by : ".ljust(30)+str(DeliveryIntegration[ctr]))
  print("Loyalty points with ".ljust(30)+str(LoyaltyIntegration[ctr]))

  if(verboseFlg != 'y' and verboseFlg != 'Y'):
    continue;


  print(' = Auth Token = \n' + str(PaymentIntegrationCredentials[ctr])[ str(PaymentIntegrationCredentials[ctr]).find(':')+1 : ])

  print("Payment Credentials  : ".ljust(30)+str(PaymentIntegrationCredentials[ctr]) + '  (RFRSH:AUTH)')
  print("POS Integration Credentials : ".ljust(30)+str(POSIntegrationCredentials[ctr]) + '  (RFRSH:AUTH)')
  print("Craver Loyalty Program ID : ".ljust(30)+str(LoyaltyProgramID[ctr]))
  print(str(LoyaltyIntegration[ctr]).rjust(6)+" Loyalty Program ID : ".ljust(24)+str(LoyaltyProgramIntegrationID[ctr]))
  print("Payment Credentials : ".ljust(30)+str(PaymentCredentialID[ctr]) )
  print("Square Merchant ID : ".ljust(30)+str(SquareMerchantID[ctr]))
  


  #List User Info
  selectUsersInfo = "select source, count(source) from users where company_fk="+str(ID[ctr])+" group by source;"
  getCursor.execute(selectUsersInfo)
  users = getCursor.fetchall()

  print("Users : ".ljust(30),end="")
  print(users)

  # list admins 
  selectAdmins = "select email, api_token, is_disabled,id from admins where company_fk = "+str(ID[ctr]) + " order by is_disabled, created_at;";

  getCursor.execute(selectAdmins)
  admins = getCursor.fetchall()

  for ctrAdmin in range(len(admins)):
    flgNIS = "";
    if(admins[ctrAdmin][2]):
      flgNIS = "(DISABLED)";

    print((str(admins[ctrAdmin][3]).rjust(4)+". Admin"+flgNIS+" : ").ljust(30)+admins[ctrAdmin][0].ljust(50),end="")
    print("API Token : "+admins[ctrAdmin][1].ljust(60))

  #List Locations
  print("\n")
  print("ID".ljust(10)+"Name (<DEL> -> DELETED!)".ljust(50)+"Location ID".ljust(40)+"Time Zone".ljust(25)+"Address".ljust(10))
  #locations
  selectLocations=""
  if(str(POSIntegration[ctr])=='SQUARE'):
    #selectLocations = "select l.id, concat(l.name,\":$->\",s.currency_code), s.square_id, l.address, l.timezone, l.is_deleted from locations l inner join square_servers s on s.id=l.square_server_id where l.company_loc_fk = "+str(ID[ctr])+" order by l.is_deleted asc;"
    selectLocations = "select concat(l.id,' ',if(c.location_fk is null,\"\",'\u2601\'),' ',if(l.delivery_credentials_id is null,\"\",'\u2690\')), concat(l.name,\":$->\",s.currency_code), s.square_id, l.address, l.timezone, l.is_deleted from locations l inner join square_servers s on s.id=l.square_server_id left join cloud_printers c on c.location_fk = l.id where l.company_loc_fk ="+str(ID[ctr])+" order by l.is_deleted asc;"
  elif(str(POSIntegration[ctr])=='TOAST'):
    #selectLocations = "select l.id, l.name, t.resturant_external_id, l.address, l.timezone, l.is_deleted  from locations l inner join pos_toast t on t.id=l.pos_credential_id where l.company_loc_fk = "+str(ID[ctr])+";" 
    selectLocations = "select concat(l.id,' ',if(c.location_fk is null,\"\",'\u2601\'),' ',if(l.delivery_credentials_id is null,\"\",'\u2690\')), l.name, t.resturant_external_id, l.address, l.timezone, l.is_deleted from locations l inner join pos_toast t on t.id=l.pos_credential_id left join cloud_printers c on c.location_fk = l.id where l.company_loc_fk = "+str(ID[ctr])+";  "
  elif(str(POSIntegration[ctr])=='CLOVER'):
    #selectLocations = "select l.id, l.name, c.merchant_id, l.address, l.timezone, l.is_deleted from locations l inner join pos_clover c on c.id=l.pos_credential_id where l.company_loc_fk ="+str(ID[ctr])+";"    
    selectLocations = "select concat(l.id,' ',if(c.location_fk is null,\"\",'\u2601\'),' ',if(l.delivery_credentials_id is null,\"\",'\u2690\')), l.name, cl.merchant_id, l.address, l.timezone, l.is_deleted from locations l inner join pos_clover cl on cl.id=l.pos_credential_id left join cloud_printers c on c.location_fk = l.id where l.company_loc_fk ="+str(ID[ctr])+";"    
  else:
    #selectLocations = "select l.id, l.name, 'NONE',l.address,l.timezone,l.is_deleted from locations l where l.company_loc_fk="+str(ID[ctr])+";"
    selectLocations = "select concat(l.id,' ',if(c.location_fk is null,\"\",'\u2601\'),' ',if(l.delivery_credentials_id is null,\"\",'\u2690\')), l.name, 'NONE',l.address,l.timezone,l.is_deleted from locations l left join cloud_printers c on c.location_fk = l.id where l.company_loc_fk="+str(ID[ctr])+";"

  selectCloudPrinters = ""

  getCursor.execute(selectLocations)
  locations = getCursor.fetchall()
  #print(locations)
  for ctrLoc in range(len(locations)):
    deleteLabel=""
    if(locations[ctrLoc][5]):
      deleteLabel = " <DEL>"
    print( (str(locations[ctrLoc][0])  ).ljust(10),end="")# u"\u2601"
    print((locations[ctrLoc][1]+deleteLabel).ljust(50),end="")
    print(str(locations[ctrLoc][2]).ljust(40),end="")
    print(str(locations[ctrLoc][4]).ljust(25),end="")
    print(str(locations[ctrLoc][3])[0:51].ljust(10))




proddb.close()



if(not proddb.is_connected()):
  print("=====================================================================================================================================================")
  print("Successfully disconnected\n")



