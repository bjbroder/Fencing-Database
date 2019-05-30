#!/usr/bin/python                                                                                           

def printAndRaise(err):
   print err
   raise Exception(err)

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"

import mysql.connector
from mysql.connector import errorcode
try:
   cnx = mysql.connector.connect(user='bbroder', password='dbkey', host='localhost', database='bbroder1')
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

cursor.execute("show columns from teams")
columns = {str(col[0]) for col in cursor.fetchall()}

if form.getvalue('delete'):
   d = form.getvalue('delete')
   if d == None:
      printAndRaise('Missing info required to delete team')
   d = str(d)

   query = "delete from teams where team_id = %s"
   cursor.execute(query, (d,))
   cnx.commit()
   print "<h2>Team with ID %s has been removed from the match.</h2>" % d
   #check if this val was in the db bc if injected then says team with id 109 even if there is none         

if form.getvalue('update'):
   u = form.getvalue('update')
   c = form.getvalue('column')
   s = form.getvalue('set')
   if None in (u,c,s):
      printAndRaise('Missing info required to update team')
   u = str(u)
   c = str(c)
   s = str(s)

   if c not in columns:
      printAndRaise('Column submitted is not a column in teams')

   query = "update teams set " + c + "= %s where team_id = %s"
   cursor.execute(query, (s,u))
   cnx.commit()
   print "<h2>%s for Team with ID %s has been updated to %s.</h2>" % (c, u, s)

if form.getvalue('id'):
   i = form.getvalue('id')
   n = form.getvalue('name')
   if None in (i,n):
      printAndRaise('Missing info required to insert new team')
   i = str(i)
   n = str(n)
   query = "select * from teams where team_id = %s"
   cursor.execute(query,(i,))
   result = cursor.fetchall()
   if len(result) != 0:
      printAndRaise('Team with this ID already exists')
   query = "insert into teams values (%s, %s, 0,0,0,0)"
   cursor.execute(query, (i,n))
   cnx.commit()
   print "<h2>Team %s with ID %s has been added to the match.</h2>" % (n,i)

if form.getvalue('attr'):
   a = form.getvalue('attr')
   t = form.getvalue('team')
   if None in (a,t):
      printAndRaise('Missing info required to display teams')
   if str(a)[0] == "[":
      aStr = ""
      for val in a:
         aStr += val + ", "
         a = aStr[:-2]

   if str(t)[0] == "[":
      tStr = ()
      for val in t:
         tStr = tStr + (str(val),)
      t = fStr
      tup = 1
   else:
      t = str(t)

   l = 1
   if tup:
      l = len(t)
      b = a.split(", ")
      for at in b:
         if at not in columns:
            printAndRaise('Column submitted is not a column in teams')
   else:
      if a not in columns:
         printAndRaise('Column submitted is not a column in teams')
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
