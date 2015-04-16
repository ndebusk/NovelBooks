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

queryStringID = "SELECT userID FROM user WHERE username = '" + str(user) + "'"
cursor2.execute(queryStringID)
for item in cursor2:
    userID = item[0]
#I build the query string in two lines because it's such a long string.
queryStringBook = "SELECT book.image, book.isbn, book.title, shoppingcartbook.format, book.price FROM book, shoppingcartbook WHERE book.isbn = shoppingcartbook.isbn AND shoppingcartbook.cartID = '" + str(userID) + "'"
cursor.execute(queryStringBook)

totalPrice = 0

print '<div class="container"><h2 class="title text-center">Shopping Cart</h2><div class="table-responsive cart_info"><table class="table table-condensed"><thead><tr class="cart_menu"><td class="image">Item</td><td class="isbn">ISBN</td><td class="description">Description</td><td class="quantity">Format</td><td class="total">Total</td><td></td></tr></thead><tbody>'
for item in cursor:
    totalPrice += item[4]
    print '<tr><td class="cart_product"><img src="%s" alt="" id="cartImage"></td>' % item[0]
    print '<td class="cart_isbn"><h5>%s</h5></td>' % item[1]
    print '<td class="cart_description"><h3>%s</h3></td>' % item[2]
    print '<td class="cart_format"><h5>%s</h5></td>' % item[3]
    print '<td class="cart_total"><p class="cart_total_price">$%s</p></td>' % item[4]
    print '<td class="cart_delete"><form id="cartItem" method="post">'
    print '<input id="isbnNum" type="hidden" name="isbnNum" value="%s"/>' % item[1]
    print '<input id="cartID" type="hidden" name="cartID" value="%s"/><button id="deleteCartItem" onclick="deleteItem()" type="button" class="btn btn-default"><i class="fa fa-times"></i></button></form></td></tr>' % userID

tax = totalPrice * decimal.Decimal(0.0825)
finalTotal = totalPrice + tax
print '</tbody></table></div></div><div class="container"><div class="row"><div class="col-sm-6"><div class="chose_area"><img src="images/home/book1.jpg" class="slideImage img-responsive" alt="" /></div></div>'
print '<div class="col-sm-6"><div class="total_area"><ul>'
print '<li>Cart Sub Total <span>$%s</span></li>' % round(totalPrice, 2)
print '<li>Tax <span>$%s</span></li>' % round(tax, 2)
print '<li>Shipping Cost <span>Free</span></li>'
print '<li>Total <span>$%s</span></li>' % round(finalTotal, 2)
print '</ul><a class="btn btn-default check_out" href="checkout.html">Check Out</a><a class="btn btn-default check_out" href="shop.html">Continue Shopping</a></div></div></div></div>'

cnx.commit()
cnx2.commit()
cnx.close()
cnx2.close();
