#!/Applications/MAMP/Library/bin/python2.7

import mysql.connector, cgi, Cookie, cookielib, os
import urllib
import urllib2


if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))

user = C['userID'].value
flag = 1
if (C.has_key("access") and C["access"].value == "admin"):
    flag = 0   


print ("Content-Type: text/html\n\n")
print flag
#if C.has_key("cookie"):
#        user_name= C['cookie'].value
#        print user_name
#        
#        #C.["testAfterHeader"] = "cookie?"
#else: 
#    print "No success!"

#print "<p>Test</p>"
#print "<p>" + str(cookie) + "</p>"
#cookie["test"] = "test"
#print "<p>" + str(cookie) + "</p>"

#form = cgi.FieldStorage()
#username = form.getvalue("username")
#password = form.getvalue("password")
#
#

#
##Creates the connection and cursor.

#
##I build the query string in two lines because it's such a long string.
##TODO: adding a non-static userID number, adding a non-static customer Name
#
#flag = 1
##for row in cursor:
##    if username == row[0] and password == row[1]:        
##        cookie['userID'] = row[0]
##        print "<p>" + str(cookie["userID"]) + "</p>"
##        if row[5] == 1:
##            cookie['access'] = "admin"
##        else:
##            cookie['access'] = "customer"
##        break
##    else:
##        continue
##print "<p>" + str(cookie) + "</p>"   
#cnx.commit()
#cnx.close();



