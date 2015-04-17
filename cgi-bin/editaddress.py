#!/Applications/MAMP/Library/bin/python2.7
import mysql.connector
import cgi
import os
import Cookie
import urllib
import urllib2

if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))
flag = 1
if (C.has_key("access") and C["access"].value == "admin"):
    flag = 0
user = C['userID'].value
form = cgi.FieldStorage()

addressID = form.getvalue("id")
keep = form.getvalue("keep")
street = form.getvalue("street")
city = form.getvalue("city")
state = form.getvalue("state")
zipCode = form.getvalue("zip")

print ("Content-Type: text/html\n\n")

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
queryString = "UPDATE `address` SET street='" + str(street) + "', city='" + str(city) + "', state='" + str(state) + "', zip='" + str(zipCode) + "' WHERE addressID ='" + str(addressID) + "'"
if (keep == "false"):    
    queryString = "DELETE FROM address WHERE addressID='" + str(addressID) + "'"
print queryString    
cursor.execute(queryString)
cnx.commit()
cnx.close()