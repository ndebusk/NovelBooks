#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi

print "<html>\
<head><title>Add Book</title></head><body>"
print "<p>Test</p>"

form = cgi.FieldStorage()

isbn = form.getvalue("isbn")
title = form.getvalue("booktitle")
publisher = form.getvalue("publisher")
price = form.getvalue("price")
pages = form.getvalue("pagenum")
description = form.getvalue("description")
image = form.getvalue("bookimage")
inStock = form.getvalue("inStock")

authors = form.getlist("author[]")
genres = form.getlist("genre[]")
formats = form.getlist("format[]")

#print to check if authors are captured from form...
for author in authors:
    print ("<p>%s</p>" % author)
for genre in genres:
    print ("<p>%s</p>" % genre)
for format in formats:
    print ("<p>%s</p>" % format)
    
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
queryStringBook = "INSERT INTO `book`(`isbn`, `title`, `publisher`, `price`, `pages`, `description`, `image`, `inStock`) VALUES "
valueStringBook = "('" + str(isbn) + "','" + str(title).replace("'", "''") + "','" + str(publisher).replace("'", "''") + "','" + str(price) + "','" + str(pages) + "','" + str(description).replace("'", "''") + "','" + str(image) + "','" + str(inStock) + "')"
queryStringBook += valueStringBook
cursor.execute(queryStringBook)

for author in authors:
    print "<p>hello</p>"
    queryStringAuthor = "INSERT INTO `author`(`author`, `isbn`) VALUES "
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
