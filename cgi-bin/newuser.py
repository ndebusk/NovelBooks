#!/Applications/MAMP/Library/bin/python2.7
print ("Content-Type: text/html\n\n")

import mysql.connector, cgi

form = cgi.FieldStorage()

realname = form.getvalue("realname")
username = form.getvalue("username")
email = form.getvalue("email")
password = form.getvalue("password")
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
cnx4 = mysql.connector.connect(**config)
cursor4 = cnx4.cursor()

queryStringTest = "SELECT username, email FROM user"
cursor2.execute(queryStringTest);
flag = 0

for user in cursor2:
    if user[0] == username:
        flag = 1
        print "Username is already taken, please select a new one."
    elif user[1] == email:
        flag = 1
        print "Email is already linked to an account, please use a different email."

#I build the query string in two lines because it's such a long string.
#TODO: adding a non-static userID number, adding a non-static customer Name
if flag == 0:
    queryString = "INSERT INTO `user`(`username`, `password`, `name`, `email`, `customer_flag`, `admin_flag`) VALUES "
    valueString = "('" + str(username) + "','" + str(password) + "','" + str(realname) +"','" + str(email) +"','1','0')"
    queryString += valueString
    cursor.execute(queryString)
    print "Account Created. Please login now."
    cnx.commit()
    cnx2.commit()
    cnx.close()
    cnx2.close()
    
    queryStringUserID = "SELECT userID FROM user WHERE username = '" + str(username) + "'"
    cursor3.execute(queryStringUserID)
    for item in cursor3:
        queryStringCreateCart = "INSERT INTO `shoppingcart`(`cartID`, `userID`) VALUES "
        valueStringCreateCart = "('" + str(item[0]) + "','" + str(item[0]) + "')"
        queryStringCreateCart += valueStringCreateCart
        cursor4.execute(queryStringCreateCart)

cnx3.commit()
cnx4.commit()

cnx3.close()
cnx4.close();
