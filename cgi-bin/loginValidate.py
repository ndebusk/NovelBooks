#!/Applications/MAMP/Library/bin/python2.7

import mysql.connector
import cgi
import Cookie
import os

#Gets the place where cookies are stored. Not sure it's needed for this particular
#script, but it will be at the top of the verification script.
if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))
form = cgi.FieldStorage()

username = form.getvalue("username")
password = form.getvalue("password")

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

#I build the query string in two lines because it's such a long string.
#TODO: adding a non-static userID number, adding a non-static customer Name
queryString = "SELECT username, password, name, email, customer_flag, admin_flag FROM user"
cursor.execute(queryString)

#Goes through the query result and prints the result.
#Flag is set to 0 if there is a match.
#The print statements set cookies.
flag = 1
for row in cursor:
    if username == row[0] and password == row[1]:        
        flag = 0
        print "Set-Cookie: userID=" + row[0]
        if row[5] == 1:
            print "Set-Cookie: access=admin"        
            break
    else:
        continue
        
#Prints the result. It is VERY important to keep the header
#line (the first print statement) here, after the query and the 
#lines above that set cookies.
print ("Content-Type: text/html\n\n")
cnx.commit()
cnx.close();
print flag


