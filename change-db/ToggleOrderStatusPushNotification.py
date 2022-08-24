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

selectNotificationSettings = "select * from notification_settings where company_id="+companyID+";"
getCursor.execute(selectNotificationSettings)
notificationSettings = getCursor.fetchall()

selectGenNotificationSettings = "select * from notification_settings order by updated_at desc limit 1;"
getCursor.execute(selectGenNotificationSettings)
genNotificationSettings = getCursor.fetchall()

tmpGenNotificationSettings = list(genNotificationSettings[0])
tmpGenNotificationSettings[0] = companyID
tmpGenNotificationSettings.pop()
tmpGenNotificationSettings.pop()
genNotificationSettings = tuple(tmpGenNotificationSettings)
print(genNotificationSettings)

if(len(notificationSettings)==0):
  if(input('Feature not active, you want to activate it ? (Y/N) - ')=='y'):
    enableOrderStatusPushNotification = "INSERT INTO notification_settings (company_id, is_enabled, processed_notification, processed_notification_title, processed_notification_body, ready_notification, ready_notification_title, ready_pick_up_notification_body, ready_delivery_notification_body, completed_notification, completed_notification_title, completed_notification_body, cancelled_notification, cancelled_notification_title, cancelled_notification_body) VALUES ("+companyID+", b'1', b'1', 'Order #%NUMBER\% is being prepared.', 'Thank you for ordering with us. Your order is being prepared now. We will notify you once it\'s ready.', b'1', 'Order #%NUMBER% is ready.', 'Your order is now ready for pickup.', 'Your order is now ready and out for delivery.', b'1', 'Order #%NUMBER\% is now completed.', 'Thanks for ordering with us. We hope to see you again soon.', b'1', 'Order #%NUMBER\% cancelled.', 'Your order has been cancelled.');"
    getCursor.execute(enableOrderStatusPushNotification)
    print(str(getCursor.rowcount) + ' rows affected')
  else:
    exit()

