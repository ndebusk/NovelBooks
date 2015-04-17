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




