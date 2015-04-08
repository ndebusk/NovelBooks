#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi

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
queryString = "SELECT username, password FROM user"
cursor.execute(queryString)

flag = 1
for row in cursor:
    if username == row[0] and password == row[1]:
        print 0
        flag = 0
        break
    else:
        continue
if flag:
    print 1
    
cnx.commit()
cnx.close();
