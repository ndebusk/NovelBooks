#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi


form = cgi.FieldStorage()

searchtype = form.getvalue("type")
searchterm = form.getvalue("term")

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

#I build the query string in two lines because it's such a long string.
#if (str(type) == "author"):
#    queryStringBook = "SELECT * FROM book"
#elif (str(type) == "isbn"):
#    #
#else:

if searchtype == "all":
    queryStringBook = "SELECT isbn, title, image, price FROM book"
    cursor.execute(queryStringBook)
    
elif searchtype == "genre":
    queryStringBook = "SELECT book.isbn, title, image, price FROM book, genre WHERE book.isbn = genre.isbn AND genre.genre = '" + searchterm + "'"
    cursor.execute(queryStringBook)
    
elif searchtype == "formatType":
    queryStringBook = "SELECT book.isbn, title, image, price FROM book, format WHERE book.isbn = format.isbn AND format.format = '" + searchterm + "'"
    cursor.execute(queryStringBook)
    
else:
    queryStringBook = "SELECT book.isbn, title, image, price FROM book, author WHERE (" + searchtype + " LIKE '%" + str(searchterm) + "%') AND (book.isbn = author.isbn)"
    cursor.execute(queryStringBook)

print '<h2 class="title text-center">%s</h2>' % searchterm
for row in cursor:
    print '<div class="col-sm-4"><div class="product-image-wrapper"><div class="single-products"><div class="productinfo text-center">'
    print '<img src="%s" alt="" />' % row[2]
    print '<h2>%s</h2>' % row[1].replace("'", "&#8217")
    queryStringAuthor = "SELECT author FROM author WHERE isbn = '" + row[0] + "'"
    cursor2.execute(queryStringAuthor)
    for item in cursor2:
        print '<p>%s</p>' %  item[0]
    print '<h5>$%s</h5>' % row[3]
    print '<form action="product-details.html" method="get"><input id="isbn" type="hidden" name="isbn" value="%s"/>' % row[0]
    print '<button id="search" type="submit" class="btn btn-default add-to-cart"><i class="fa fa-bars"></i>Details</button></form></div></div></div></div>'
    cnx2.commit()
cnx.commit()
cnx.close()
cnx2.close();
