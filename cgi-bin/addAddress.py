#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi, Cookie, cookielib, os, decimal
import urllib
import urllib2

if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))

user = C['userID'].value

form = cgi.FieldStorage()

city = form.getvalue("city")
state = form.getvalue("state")
street = form.getvalue("street")
zipcode = form.getvalue("zip")

    
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
cursor2 = cnx.cursor()

queryStringID = "SELECT userID FROM user WHERE username = '" + str(user) + "'"
cursor2.execute(queryStringID)
for item in cursor2:
    userID = item[0]
#I build the query string in two lines because it's such a long string.
queryString = "INSERT INTO `address`(`userID`, `street`, `city`, `state`, `zip`) VALUES "
valueString = "('" + str(userID) + "','" + str(street) + "','" + str(city) + "','" + str(state) + "','" + str(zipcode) + "')"
queryString += valueString
cursor.execute(queryString)

print "<p>Address Saved!</p>"
    
cnx.commit()
cnx.close();
