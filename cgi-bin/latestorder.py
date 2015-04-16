#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi, Cookie, cookielib, os
import urllib
import urllib2
import datetime

form = cgi.FieldStorage()

total = form.getvalue("total")
address = form.getvalue("address")
status = "pending"
if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))

user = C['userID'].value
    
#Sets my config for accessing the database. MAMP gave two different
#ways for accessing the database, but I seemed to have trouble
#connecting without using the UNIX socket.
config = {
  'user': 'root',
  'password': 'root',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'database': 'NovelBooks',
  'raise_on_warnings': True,
}

#Creates the connection and cursor.
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()


userID = -1
queryStringID = "SELECT userID FROM user WHERE username = '" + str(user) + "'"
cursor.execute(queryStringID)
for item in cursor:
    userID = item[0]
cnx.commit()



queryStringOrderNum = "SELECT MAX(orderNum) FROM `order` WHERE userID='" + str(userID) + "'"
cursor.execute(queryStringOrderNum)
orderNum = -1
for item in cursor:
    orderNum = item[0]
print orderNum
cnx.commit()
cnx.close()
