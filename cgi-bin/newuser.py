#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi

print "<html>\
<head><title>Login</title></head><body>"
print "<p>Test</p>"

form = cgi.FieldStorage()
realname = form.getvalue("realname")
username = form.getvalue("username")
email = form.getvalue("email")
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
queryString = "INSERT INTO `user`(`username`, `password`, `name`, `email`, `customer_flag`, `admin_flag`) VALUES "
valueString = "('" + str(username) + "','" + str(password) + "','" + str(realname) +"','" + str(email) +"','1','0')"
queryString += valueString
cursor.execute(queryString)
cnx.commit()
cnx.close();