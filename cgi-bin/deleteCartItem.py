#!/Applications/MAMP/Library/bin/python2.7
import mysql.connector
import cgi
import os
import Cookie
import urllib
import urllib2

print ("Content-Type: text/html\n\n")

form = cgi.FieldStorage()
 
isbn = form.getvalue("isbnNum")
cartID = form.getvalue("cartID")

#Keeps the password for being overwritten if the user does not put anything in
#that field

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

deleteString = "DELETE FROM shoppingcartbook WHERE isbn='" + str(isbn) + "' AND cartID='" + str(cartID) + "'"
cursor.execute(deleteString)
cnx.commit()
cnx.close();
