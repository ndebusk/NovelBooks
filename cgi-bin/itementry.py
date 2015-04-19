#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi

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

if inStock != '1':
    inStock = '0';
    
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
cnx2 = mysql.connector.connect(**config)
cursor2 = cnx2.cursor()
flag = 0
queryString = "SELECT isbn FROM book"
cursor2.execute(queryString);
for item in cursor2:
    if isbn == item[0]:
        print "Duplicate ISBN numbers found. Please correct your ISBN number."
        flag = 1

if flag == 0:
    #I build the query string in two lines because it's such a long string.
    queryStringBook = "INSERT INTO `book`(`isbn`, `title`, `publisher`, `price`, `pages`, `description`, `image`, `inStock`) VALUES "
    valueStringBook = "('" + str(isbn) + "','" + str(title).replace("'", "''") + "','" + str(publisher).replace("'", "''") + "','" + str(price) + "','" + str(pages) + "','" + str(description).replace("'", "''") + "','" + str(image) + "','" + str(inStock) + "')"
    queryStringBook += valueStringBook
    cursor.execute(queryStringBook)

    for author in authors:
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

    print "Item successfully added!"

cnx.commit()
cnx2.commit()
cnx.close()
cnx2.close();
