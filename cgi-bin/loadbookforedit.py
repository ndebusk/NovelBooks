#!/Applications/MAMP/Library/bin/python2.7
import mysql.connector
import cgi
import os
import Cookie
import urllib
import urllib2

if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))

isbn = "0756404746"
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
queryStringBook = "SELECT title, publisher, price, pages, description, image, instock FROM book WHERE isbn='" + str(isbn) + "'"
queryStringAuthor = "SELECT author FROM author WHERE isbn='" + str(isbn) + "'"
queryStringGenre = "SELECT genre FROM genre WHERE isbn='" + str(isbn) + "'"
queryStringFormat = "SELECT format FROM format WHERE isbn='" + str(isbn) + "'"

cursor.execute(queryStringBook)

for row in cursor:
    print "<p>" + row[0] + "</p>"    
cursor.execute(queryStringAuthor)
for row in cursor:
    print "<p>" + row[0] + "</p>"
cursor.execute(queryStringGenre)
for row in cursor:
    print "<p>" + row[0] + "</p>"
cursor.execute(queryStringFormat)
for row in cursor:
    print "<p>" + row[0] + "</p>"

cnx.commit()
cnx.close();