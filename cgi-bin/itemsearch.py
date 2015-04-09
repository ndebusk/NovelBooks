#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi

print "<html>\
<head><title>Results</title></head><body>"
print "<p>Results page (test only)</p>"
print "<p>Results should ultimately be put on the correct page.<p>"

form = cgi.FieldStorage()

#searchterm = form.getvalue("searchterm")
searchtype = "title"
searchterm = "The Name of the Wind"
   
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
queryStringBook = "SELECT * FROM book WHERE " + searchtype + " LIKE '%" + str(searchterm) + "%';"
#queryStringBook = "SELECT * FROM book WHERE title LIKE '%Name%'"
cursor.execute(queryStringBook)


for row in cursor:
    print '<h2 class="title text-center">Products</h2><div class="col-sm-4"><div class="product-image-wrapper"><div class="single-products"><div class="productinfo text-center">'
    print '<img src="%s" alt="" />' % row[2]
    print '<h2>%s</h2>' % row[1]
    print '<p>%s</p>' %  row[0]
    print '<a href="#" class="btn btn-default add-to-cart"><i class="fa fa-shopping-cart"></i>Add to cart</a></div></div></div></div>'
cnx.commit()
cnx.close();

