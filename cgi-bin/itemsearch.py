#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi

print "<html>\
<head><title>Results</title></head><body>"
print "<p>Results page (test only)</p>"
print "<p>Results should ultimately be put on the correct page.<p>"

form = cgi.FieldStorage()

searchterm = form.getvalue("searchterm")
searchtype = "title"

    
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
queryStringBook = "SELECT * FROM `book` WHERE '" + searchtype + "'='" + str(searchterm) + "';"
cursor.execute(queryStringBook)
print "<p>Made it past the query<p>"   
cnx.commit()
cnx.close();
