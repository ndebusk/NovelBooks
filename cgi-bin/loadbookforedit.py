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
isbn = "0756404746"
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
if (flag == 0):
    #I build the query string in two lines because it's such a long string.
    queryStringBook = "SELECT title, publisher, price, pages, description, image, instock FROM book WHERE isbn='" + str(isbn) + "'"
    queryStringAuthor = "SELECT author FROM author WHERE isbn='" + str(isbn) + "'"
    queryStringGenre = "SELECT genre FROM genre WHERE isbn='" + str(isbn) + "'"
    queryStringFormat = "SELECT format FROM format WHERE isbn='" + str(isbn) + "'"

    cursor.execute(queryStringBook)
    
    for row in cursor:
        #found = 1
        print '<h2 class="title text-center">Edit Book Info</h2>'
        print '<div class="row">'
        print '<div class="col-sm-8">'
        print '<div class="item-entry">'
        print '<p>Click on a box to edit that value.</p>'
        print '<p><form id="booksubmit" action="/cgi-bin/updateBook.py" method="post"></p>'
        print '<p><input id="isbn" type="text" name="isbn" value="' + str(isbn) + '"/></p>'
        print '<p><input id="newtitle" type="text" name="newtitle" value="' + str(row[0]) + '"/></p>'
        print '<p><input id="newpublisher" type="text" name="newpublisher" value="' + str(row[1]) + '"/></p>'
        print '<p><input id="newprice" type="text" name="newprice" value="' + str(row[2]) + '"/></p>'
        print '<p><input id="newpages" type="text" name="newpages" value="' + str(row[3]) + '"/></p>'
        print '<p><input id="newdesc" type="text" name="newdesc" value="' + str(row[4]) + '"/></p>'
        print '<p><input id="newimage" type="text" name="newimage" value="' + str(row[5]) + '"/></p>'    
        print '<span id="stockspan">'
        print '<input id="instock" type="checkbox" name="inStock" class="checkbox" value="' + str(row[6]) + '">'
        print 'Check if book is now in stock.</br>'
        print '</span>'
    
    cursor.execute(queryStringAuthor)
    for row in cursor:
        print '<input type="text" name="author[]" value="' + row[0] + '" />'
    print '<button class="expanderbutton" type="button" class="btn btn-default">Add Another Author</button></br>'

    cursor.execute(queryStringGenre)
    for row in cursor:
        print '<input type="text" name="genre[]" value="' + row[0] + '"/>'
    print '<button class="expanderbutton" type="button" class="btn btn-default">Add Another Genre</button></br>'

    cursor.execute(queryStringFormat)
    print '<span id="formatspan">'
    print 'Check each available book format: <br/>'


    for row in cursor:
        print row[0] + '<input type="checkbox" name="format[]" value="' + row[0] + '" /><br/>'

    print '</span>'
    print '<button id="updateBookSubmit" type="button" class="btn btn-default">Save Book Changes</button>'
    print '<button id="deleteBookSubmit" type="button" class="btn btn-default">Delete Book From Database</button>'
    print '</form>'
    print '</div></div></div>'
    cnx.commit()
cnx.close();