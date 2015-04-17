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

isbn = form.getvalue("isbn")
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
queryStringUser = "SELECT userID FROM user WHERE username='" + str(user) + "'"
cursor.execute(queryStringUser)
userID = -1
for row in cursor:
    userID = row[0]
    
queryStringAddress = "SELECT * FROM address WHERE userID = '" + str(userID) + "'"
cursor.execute(queryStringAddress)

print '<div class="styled-select3 blue semi-square"><select id="userAddress">'
for row in cursor:
    address = str(row[2] + " " + row[3] + ", " + row[4] + " " + row[5]).replace("'", "''")
    print '<option value="%s">' % address
    print '%s</option>' % address
print '</div>'
cnx.close();