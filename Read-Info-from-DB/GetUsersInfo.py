import mysql.connector
import requests
import time
import csv

#inputs
# Check for company info
exec(open('Read-Info-from-DB/GetCompanyInfo.py').read())
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

