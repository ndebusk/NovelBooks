#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi, Cookie, cookielib, os, decimal
import urllib
import urllib2

if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))
    user = C['userID'].value
else:
    user = ''

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
ebookFormat = 0
printFormat = 0
for formatType in cursorFormat:
    f.append(formatType[0])
    if formatType[0] == "ebook":
        ebookFormat = 1
    elif formatType[0] == "print":
        printFormat = 1
loggedIn = 1
if user == '':
    loggedIn = 0
    
aString = ", ".join(a)
gString = ", ".join(g)
fString = ", ".join(f)

for book in cursorBook:
    if book[7] > 0 and printFormat == 1:
        available = "In Stock"
    else:
        available = "Out of Stock"
        printFormat = 0
    print '<div class="col-sm-5"><div class="view-product">'
    print '<img src="%s" alt="" />' % book[6]
    print '</div></div><div class="col-sm-7"><div class="product-information"><!--/product-information-->'
    print '<h1>%s</h1>' % book[1]
    print '<h2>%s</h2>' % aString.replace("'", "&#8217")
    print '<p>ISBN: %s</p>' % book[0]
    print '<span><span>$ %s</span></span>' % book[3]
    print '<p><b>Availability:</b> %s</p>' % available
    print '<div><form id="addToCart" method="post">'
    print '<input id="isbnVal" type="hidden" name="isbnVal" value="%s"/>' % book[0]
    print '<fieldset class="group"><ul class="checkbox">'
    if ebookFormat == 1:
        print '<li><input type="checkbox" id="ebook" name="format[]" value="ebook" /><label for="ebook">eBook</label></li>'
    if printFormat == 1:
        print '<li><input type="checkbox" id="print" name="format[]" value="print" /><label for="print">Print</label></li>'
    print '</ul></fieldset>'
    if loggedIn == 0:
        print "<p>Please login to add items.</p>"
    else:
        print '<button id="addCart" onclick="addToCart()" type="button" class="btn btn-default cart"><i class="fa fa-shopping-cart"></i> Add to cart</button>'
    print '</form></div></div><!--/product-information--></div><div class="col-sm-12"><div class="product-information"><!--/product-information--><h2 class="title text-center">Details</h2>'
    print '<p><b>Publisher:</b> %s</p>' % book[2].replace("'", "&#8217")
    print '<p><b>Genre:</b> %s</p>' % gString
    print '<p><b>Pages:</b> %s</p>' % book[4]
    print '<p><b>Format:</b> %s</p>' % fString
    print "<p><b>Description:</b> %s</p>" % book[5].replace("'", "&#8217")
    print '</div><!--/product-information--></div>'

cnxb.commit()
cnxa.commit()
cnxg.commit()
cnxf.commit()
cnxb.close()
cnxa.close()
cnxg.close()
cnxf.close();
