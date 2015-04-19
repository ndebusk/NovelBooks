#!/Applications/MAMP/Library/bin/python2.7
import mysql.connector
import cgi
import os
import Cookie
import urllib
import urllib2

if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))
flag = 1
if (C.has_key("access") and C["access"].value == "admin"):
    flag = 0

form = cgi.FieldStorage()

isbn = form.getvalue("isbn")
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
found = 0
if (flag == 0):
    #I build the query string in two lines because it's such a long string.
    queryStringBook = "SELECT title, publisher, price, pages, description, image, instock FROM book WHERE isbn='" + str(isbn) + "'"
    queryStringAuthor = "SELECT author FROM author WHERE isbn='" + str(isbn) + "'"
    queryStringGenre = "SELECT genre FROM genre WHERE isbn='" + str(isbn) + "'"
    queryStringFormat = "SELECT format FROM format WHERE isbn='" + str(isbn) + "'"

    cursor.execute(queryStringBook)
    
    for row in cursor:
        found = 1
        inStockVal = row[6]
        print '<h2 class="title text-center">Edit Book Info</h2>'
        print '<div class="row">'
        print '<div class="col-sm-8">'
        print '<div class="item-entry">'
        print '<p>Click on a box to edit that value.</p>'
        print '<p><form id="booksubmit" method="post"></p>'
        print '<p><input id="isbn" type="text" name="isbn" value="' + str(isbn) + '"/></p>'
        print '<p><input id="newtitle" type="text" name="newtitle" value="' + str(row[0]).replace("'", "&#8217") + '"/></p>'
        print '<p><input id="newpublisher" type="text" name="newpublisher" value="' + str(row[1]).replace("'", "&#8217") + '"/></p>'
        print '<p><input id="newprice" type="text" name="newprice" value="' + str(row[2]) + '"/></p>'
        print '<p><input id="newpages" type="text" name="newpages" value="' + str(row[3]) + '"/></p>'
        print '<p><input id="newdesc" type="text" name="newdesc" value="' + str(row[4]).replace("'", "&#8217") + '"/></p>'
        print '<p><input id="newimage" type="text" name="newimage" value="' + str(row[5]) + '"/></p>'
    if (found == 1):
        cursor.execute(queryStringAuthor)
        for row in cursor:
            print '<input type="text" name="author[]" value="' + row[0] + '" />'
        print '<button class="expanderbutton" type="button" class="btn btn-default">Add Another Author</button></br>'

        cursor.execute(queryStringGenre)
        for row in cursor:
            print '<input type="text" name="genre[]" value="' + row[0] + '"/>'
        print '<button class="expanderbutton" type="button" class="btn btn-default">Add Another Genre</button></br>'

        cursor.execute(queryStringFormat)
        inStock = ''
        if inStockVal == 1:
            inStock = "checked"
        ebook = ''
        printFormat = ''
        print '<span id="formatspan"><h5>In Stock Options: <h5></span><fieldset class="group"><ul class="checkbox">'
        for row in cursor:
            if row[0] == "ebook":
                ebook = "checked"
            if row[0] == "print":
                printFormat = "checked"

        print '<li><input type="checkbox" id="ebook" name="format[]" value="ebook" ' +ebook+ ' /><label for="ebook">eBook</label></li>'
        print '<li><input type="checkbox" id="print" name="format[]" value="print" ' +printFormat+ ' /><label for="ebook">Print</label></li>'
        print '<li><input type="checkbox" id="instock" name="inStock" class="checkbox" value="1" ' +inStock+ '/><label for="instock">In Stock</label></li></ul></fieldset>'
        
        print '<button id="updateBookSubmit" type="button" class="btn btn-default">Save Book Changes</button></br>'
        print '<button id="deleteBookSubmit" type="button" class="btn btn-default">Delete Book From Database</button></br>'
        print '</form>'
        print '</div></div></div>'
    else:
        print 0

cnx.commit()
cnx.close();