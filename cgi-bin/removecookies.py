#!/Applications/MAMP/Library/bin/python2.7

import mysql.connector, cgi, Cookie, cookielib, os
import urllib
import urllib2


if os.environ.has_key("HTTP_COOKIE"):
    C= Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))

user = C['userID'].value

  
print "Set-Cookie: userID=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT"
print "Set-Cookie: access=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT"

print ("Content-Type: text/html\n\n")





