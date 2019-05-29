#!/usr/bin/python                                                                                        

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"

import mysql.connector
from mysql.connector import errorcode
try:
   cnx = mysql.connector.connect(user='bbroder', password='dbkey', host='localhost', database='bbroder1'\
)
except mysql.connector.Error as err:
   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print 'Invalid credential. Unable to access database.'
   elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print 'Database does not exists'
   else:
        print 'Failed to connect to database'
try:
   cursor = cnx.cursor()
except mysql.connector.Error as err:

    print "Error:", err.message

    # close connection                                                                                   
    cnx.close()

# Import modules for CGI handling                                                                        
import cgi, cgitb

# Create instance of FieldStorage                                                                        
form = cgi.FieldStorage()

d = u = c = i = n = a = t = tup = 0

# Get data from fields                                                                                   
if form.getvalue('delete'):
   d = str(form.getvalue('delete'))

if form.getvalue('update'):
   u = str(form.getvalue('update'))
   c = str(form.getvalue('column'))
   s = str(form.getvalue('set'))
    
if form.getvalue('id'):
   i = str(form.getvalue('id'))
   n = str(form.getvalue('name'))

if form.getvalue('attr') and form.getvalue('team'):
   a = form.getvalue('attr')
   t = form.getvalue('team')
   if str(a)[0] == "[":
      aStr = ""
      for val in a:
         aStr += val + ", "
      a = aStr[:-2]

   if str(t)[0] == "[":
      tStr = ()
      for val in t:
         tStr = tStr + (str(val),)
      t = tStr
      tup = 1
   else:
      t = str(t)                                 
      
if d:
   query = "delete from teams where team_id = %s"
   cursor.execute(query, (d,))
   cnx.commit()
   print "<h2>Team with ID %s has been removed from the match.</h2>" % d
 
  
if u:
   query = "update teams set " + c + "=" + s + " where team_id = %s"
   cursor.execute(query, (u,))
   cnx.commit()
   print "<h2>%s for Team with ID %s has been updated to %s.</h2>" % (c, u, s)

if i:
   query = "insert into teams values (" + i + ", %s, 0,0,0)"
   cursor.execute(query, (n,))
   cnx.commit()
   print "<h2>Team %s with ID %s has been added to the match.</h2>" % (n,i)

if a:
   l = 1
   if tup:
      l = len(t)
   query = "select " + a + " from teams where team_id in (" + ("%s, " * l)
   query = query[:-2] + ")"
   if tup:
      cursor.execute(query, t)
   else:
      cursor.execute(query, (t,))
   print "Data returned from columns " + a + ":"
   for res in cursor:
      print "<br>"
      if type(res) == type(()):
         print "|"
         for r in res:
            print r
            print "|"

print "</body>"
print "</html>"

cursor.close()
cnx.close()
