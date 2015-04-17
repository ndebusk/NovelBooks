#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi, Cookie, cookielib, os, decimal
import urllib
import urllib2
import datetime

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
cursor.execute(queryStringID)
for item in cursor:
    userID = item[0]

queryStringOrder = "SELECT * FROM novelbooks.`order` WHERE userID = '" + str(userID) + "'"
cursor2.execute(queryStringOrder)

for order in cursor2:
    date = datetime.datetime.strptime(str(order[1]), '%Y-%m-%d')
    formatDate = datetime.date.strftime(date, "%B %d, %Y")
    print '<div class="table-responsive cart_info"><table class="table table-condensed"><thead>'
    print '<tr class="cart_menu"><td class="heading">Order Number: %s</td>' % order[0]
    print '<td class="heading">%s</td>' % formatDate
    print '<td class="heading">%s</td>' % order[3]
    print '<td class="heading">$%s</td>' % order[2]
    print '<td class="heading">Status: %s</td></tr></thead><tbody>' % order[4]
    queryStringItem = "SELECT lineItemNum, isbn, quantity, format, itemPrice FROM orderitem WHERE orderitem.orderNum = '" + str(order[0]) + "'"
    cursor3.execute(queryStringItem)
    for item in cursor3:
        print '<tr><td class="item"><h5>%s</h5></td>' % item[0]
        print '<td class="item"><h5>ISBN: %s</h5></td>' % item[1]
        print '<td class="item"><h5>Quantity: %s</h5></td>' % item[2]
        print '<td class="item"><h5>%s</h5></td>' % item[3]
        print '<td class="item"><h5>$%s</h5></td></tr>' % item[4]
    print '</tbody></table></div>'

cnx.commit()
cnx2.commit()
cnx3.commit()
cnx.close()
cnx2.close()
cnx3.close();
