#!/Applications/MAMP/Library/bin/python2.7
import mysql.connector
import cgi
import os
import Cookie
import urllib
import urllib2

if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))

user = C['userID'].value
user = "sean"

print ("Content-Type: text/html\n\n")

form = cgi.FieldStorage()

realname = form.getvalue("name")
email = form.getvalue("email")
newpassword = form.getvalue("newpassword")
oldpassword = form.getvalue("password")
#Keeps the password for being overwritten if the user does not put anything in
#that field
if (newpassword == None):    
    newpassword = oldpassword


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
#need to add the password check here
queryStringUser = "SELECT userID FROM user WHERE username='" + str(user) + "' AND password='" + str(oldpassword) + "'"
cursor.execute(queryStringUser)
userNum = -1
for row in cursor:
    userNum = row[0]    
##I build the query string in two lines because it's such a long string.
if (userNum != -1):
    queryStringUpdate = "UPDATE user SET name='" + str(realname) + "', " + "password='" + str(newpassword) + "', " + "email='" + str(email) + "' WHERE userID='" + str(userNum) + "';"
    cursor.execute(queryStringUpdate)    
print userNum
cnx.commit()
cnx.close();