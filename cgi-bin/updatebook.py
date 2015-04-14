#!/Applications/MAMP/Library/bin/python2.7
import mysql.connector
import cgi
import os
import Cookie
import urllib
import urllib2

if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))



print ("Content-Type: text/html\n\n")

form = cgi.FieldStorage()

        
isbn = form.getvalue("isbn")
title = form.getvalue("newtitle")
publisher = form.getvalue("newpublisher")
price = form.getvalue("newprice")
pages = form.getvalue("newpages")
description = form.getvalue("newdesc")
image = form.getvalue("newimage")
inStock = form.getvalue("inStock")

authors = form.getlist("author[]")
genres = form.getlist("genre[]")
formats = form.getlist("format[]")

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
queryStringBook = "UPDATE `book` SET title='" + str(title) + "', publisher='" + str(publisher) + "', price ='" + str(price) + "', pages='" + str(pages) + "', description='" + str(description) + "', image='" + str(image) + "', instock ='" + str(instock) + "' WHERE isbn='" + str(isbn) + "'"
#valueStringBook = "isbn= str(isbn) + "','" + str(title).replace("'", "''") + "','" + str(publisher).replace("'", "''") + "','" + str(price) + "','" + str(pages) + "','" + str(description).replace("'", "''") + "','" + str(image) + "','" + str(inStock) + "')"
#queryStringBook += valueStringBook
cursor.execute(queryStringBook)

for author in authors:
    queryStringAuthor = "UPDATE `author` SET author= '
    valueStringAuthor = "('" + str(author) + "','" + str(isbn) + "')"
    queryStringAuthor += valueStringAuthor
    cursor.execute(queryStringAuthor)

for genre in genres:
    queryStringGenre = "INSERT INTO `genre`(`genre`, `isbn`) VALUES "
    valueStringGenre = "('" + str(genre) + "','" + str(isbn) + "')"
    queryStringGenre += valueStringGenre
    cursor.execute(queryStringGenre)
    
for formatType in formats:
    queryStringFormat = "INSERT INTO `format`(`format`, `isbn`) VALUES "
    valueStringFormat = "('" + str(formatType) + "','" + str(isbn) + "')"
    queryStringFormat += valueStringFormat
    cursor.execute(queryStringFormat)
cnx.commit()
cnx.close();