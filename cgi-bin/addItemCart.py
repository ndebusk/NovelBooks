#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi, Cookie, cookielib, os
import urllib
import urllib2

form = cgi.FieldStorage()

isbn = form.getvalue("isbnVal")
formats = form.getlist("format[]")
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

queryStringCartID = "SELECT shoppingcart.cartID FROM shoppingcart, user WHERE user.userID = shoppingcart.userID AND user.username = '" + str(user) + "'"
cursor2.execute(queryStringCartID)
for item in cursor2:
    cartID = item[0]
#I build the query string in two lines because it's such a long string.
for formatType in formats:
    queryStringInsertCart = "INSERT INTO `shoppingcartbook`(`cartID`, `isbn`, `format`) VALUES "
    valueStringInsertCart = "('" + str(cartID) + "','" + str(isbn) + "','" + str(formatType) + "')"
    queryStringInsertCart += valueStringInsertCart
    cursor.execute(queryStringInsertCart)
    
cnx.commit()
cnx2.commit()
cnx.close()
cnx2.close();
