#!/Applications/MAMP/Library/bin/python2.7
import mysql.connector
import cgi

print "Content-Type: text/html"
print 
print "<html>\
<head><title>Results</title></head><body>"

form = cgi.FieldStorage()

isbn = form.getvalue("isbn")

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
cnxb = mysql.connector.connect(**config)
cnxa = mysql.connector.connect(**config)
cnxg = mysql.connector.connect(**config)
cnxf = mysql.connector.connect(**config)
cursorBook = cnxb.cursor()
cursorAuthor = cnxa.cursor()
cursorGenre = cnxg.cursor()
cursorFormat = cnxf.cursor()

#I build the query string in two lines because it's such a long string.
queryStringBook = "SELECT * FROM book WHERE isbn = " + isbn
cursorBook.execute(queryStringBook)

queryStringAuthor = "SELECT author FROM author WHERE isbn = " + isbn
cursorAuthor.execute(queryStringAuthor)
a = []
for author in cursorAuthor:
    a.append(author[0])

queryStringGenre = "SELECT genre FROM genre WHERE isbn = " + isbn
cursorGenre.execute(queryStringGenre)
g = []
for genre in cursorGenre:
    g.append(genre[0])

queryStringFormat = "SELECT format FROM format WHERE isbn = " + isbn
cursorFormat.execute(queryStringFormat)
f = []
for formatType in cursorFormat:
    f.append(formatType[0])
    
aString = ", ".join(a)
gString = ", ".join(g)
fString = ", ".join(f)

for book in cursorBook:
    if book[7] > 0:
        available = "In Stock"
    else:
        available = "Out of Stock"
    print '<div class="col-sm-5"><div class="view-product">'
    print '<img src="%s" alt="" />' % book[6]
    print '</div></div><div class="col-sm-7"><div class="product-information"><!--/product-information-->'
    print '<h1>%s</h1>' % book[1]
    print '<h2>%s</h2>' % aString
    print '<p>ISBN: %s</p><span>' % book[0]
    print '<span>$ %s</span>' % book[3]
    print '<button type="button" class="btn btn-default cart"><i class="fa fa-shopping-cart"></i> Add to cart</button></span>'
    print '<p><b>Availability:</b> %s</p>' % available
    print '</div><!--/product-information--></div><div class="col-sm-12"><div class="product-information"><!--/product-information--><h2 class="title text-center">Details</h2>'
    print '<p><b>Publisher:</b> %s</p>' % book[2]
    print '<p><b>Genre:</b> %s</p>' % gString
    print '<p><b>Pages:</b> %s</p>' % book[4]
    print '<p><b>Format:</b> %s</p>' % fString
    print "<p><b>Description:</b> %s</p>" % book[5]
    print '</div><!--/product-information--></div>'

cnxb.commit()
cnxa.commit()
cnxg.commit()
cnxf.commit()
cnxb.close()
cnxa.close()
cnxg.close()
cnxf.close();
