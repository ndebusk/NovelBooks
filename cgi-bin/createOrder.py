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
cnx2 = mysql.connector.connect(**config)
cursor2 = cnx2.cursor()

queryStringID = "SELECT userID FROM user WHERE username = '" + str(user) + "'"
cursor.execute(queryStringID)
for item in cursor:
    userID = item[0]
cnx.commit()

i = datetime.datetime.now()
date = "%s/%s/%s" % (i.day, i.month, i.year)

queryStringInsertCart = "INSERT INTO `order`(`date`, `total`, `shippingAddress`, `orderStatus`, `userID`) VALUES "
valueStringInsertCart = "(CURDATE(),'" + str(total) + "','" + str(address) + "','" + str(status) + "','" + str(userID) + "')"
queryStringInsertCart += valueStringInsertCart
cursor.execute(queryStringInsertCart)
cnx.commit()

queryStringOrderNum = "SELECT orderNum FROM novelbooks.`order` WHERE date = CURDATE() AND total = '" + str(total) + "' AND shippingAddress = '" + str(address) + "' AND orderStatus = '" + str(status) + "' AND userID = '" + str(userID) + "'"
cursor.execute(queryStringOrderNum)
for item in cursor:
    orderNum = item[0]
cnx.commit()

queryStringCart = "SELECT isbn, format FROM shoppingcartbook WHERE cartID = '" + str(userID) + "'"
cursor.execute(queryStringCart)

quantity = 1
lineItem = 1
for item in cursor:
    queryStringInsertOrder = "INSERT INTO `orderitem`(`isbn`, `orderNum`, `lineItemNum`, `quantity`, `format`) VALUES "
    valueStringInsertOrder = "('" + str(item[0]) + "','" + str(orderNum) + "','" + str(lineItem) + "','" + str(quantity) + "','" + str(item[1]) +"')"
    queryStringInsertOrder += valueStringInsertOrder
    cursor2.execute(queryStringInsertOrder)

cnx.commit()

deleteString = "DELETE FROM shoppingcartbook WHERE cartID='" + str(userID) + "'"
cursor.execute(deleteString)
    
cnx.commit()
cnx2.commit()
cnx.close()
cnx2.close();
