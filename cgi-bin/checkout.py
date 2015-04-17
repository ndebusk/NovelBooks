#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi, Cookie, cookielib, os, decimal
import urllib
import urllib2

if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))

user = C['userID'].value
    
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
cnx3 = mysql.connector.connect(**config)
cursor3 = cnx3.cursor()

queryStringID = "SELECT userID FROM user WHERE username = '" + str(user) + "'"
cursor2.execute(queryStringID)
for item in cursor2:
    userID = item[0]

queryStringAddress = "SELECT * FROM address WHERE userID = '" + str(userID) + "'"
cursor3.execute(queryStringAddress)
#I build the query string in two lines because it's such a long string.
queryStringBook = "SELECT book.image, book.isbn, book.title, shoppingcartbook.format, book.price FROM book, shoppingcartbook WHERE book.isbn = shoppingcartbook.isbn AND shoppingcartbook.cartID = '" + str(userID) + "'"
cursor.execute(queryStringBook)

totalPrice = 0

print '<div class="table-responsive cart_info"><table class="table table-condensed"><thead><tr class="cart_menu"><td class="image">Item</td><td class="isbn">ISBN</td><td class="description">Description</td><td class="format">Format</td><td class="total">Total</td></tr></thead><tbody>'
for item in cursor:
    totalPrice += item[4]
    print '<tr><td class="cart_product"><img src="%s" alt="" id="checkoutImage"></td>' % item[0]
    print '<td class="cart_isbn"><h4>%s</h4></td>' % item[1]
    print '<td class="cart_description"><h4>%s</h4></td>' % item[2]
    print '<td class="cart_format"><h4>%s</h4></td>' % item[3]
    print '<td class="cart_total"><p class="cart_total_price">$%s</p></td></tr>' % item[4]

tax = totalPrice * decimal.Decimal(0.0825)
finalTotal = totalPrice + tax

print '<tr><td colspan="4">&nbsp;</td><td colspan="2"><table class="table table-condensed total-result">'
print '<tr><td>Cart Sub Total</td><td>$%s</td></tr>' % round(totalPrice, 2)
print '<tr><td>Tax</td><td>$%s</td></tr>' % round(tax, 2)
print '<tr class="shipping-cost"><td>Shipping Cost</td><td>Free</td></tr>'
print '<tr><td>Total</td><td><span>$%s</span></td></tr>' % round(finalTotal, 2)
print '</table></td></tr></tbody></table></div>'

print '<div class="container"><div class="row"><div class="col-sm-12"><h2 class="title text-center">Shipping Address</h2><div class="col-sm-6"><form id="addToOrder" method="post">'
print '<input id="totalVal" type="hidden" name="totalVal" value="%s"/>' % round(finalTotal, 2)
print '<div class="styled-select2 blue semi-square"><select id="userAddress">'
for item in cursor3:
    address = str(item[2] + " " + item[3] + ", " + item[4] + " " + item[5]).replace("'", "''")
    print '<option value="%s">' % address
    print '%s</option>' % address

print '</select></div><a class="btn btn-default check_out" href="addaddress.html">Manage Addresses</a>'
print '<button id="submitOrder" onclick="addToOrder()" type="button" class="btn btn-default check_out">Submit Order</button></form></div></div></div></div>'

cnx.commit()
cnx2.commit()
cnx3.commit()
cnx.close()
cnx2.close()
cnx3.close();

