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

#I build the query string in two lines because it's such a long string.
queryStringBook = "SELECT username, name, email FROM user WHERE username='" + str(user) + "'"
cursor.execute(queryStringBook)

for row in cursor:
    print '<h2 class="title text-center">User Info: ' + str(row[0]) + '</h2>'
    print '<div class="row">'
    print '<div class="col-sm-8">'
    print '<div class="item-entry">'
    print '<p>Click on a box to edit that value.</p>'
    print '<p><form action="/cgi-bin/updateCustomer.py" method="post"></p>'
    print '<p><input id="newpassword" type="password" name="newpassword" placeholder="Enter new password"/></p>'
    print '<p><input id="name" type="text" name="name" value="' + str(row[1]) + '"/></p>'
    print '<p><input id="email" type="text" name="email" value="' + str(row[2]) + '"/></p>'    
print '<input id="password" type="password" name="password" placeholder="Enter your current password to confirm new changes"/></p>'    
print '<button id="updateUserSubmit" type="button" class="btn btn-default">Save User Changes</button></p>'
print '</form>'
print '</div></div></div>'

cnx.commit()
cnx.close();