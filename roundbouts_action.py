#!/usr/bin/python                                                                               \
                                                                                                 
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
   cnx = mysql.connector.connect(user='bbroder', password='dbkey', host='localhost', database='b\
broder1'\
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
    cnx.close()
 
import cgi, cgitb
 
form = cgi.FieldStorage()
 
d = u = c = i = n = t = sq = a = f = tup = 0
 
cursor.execute("show columns from fencers")
columns = {str(col[0]) for col in cursor.fetchall()}
 
if form.getvalue('delete'):
    d = form.getvalue('delete')
    if d == None:
        printAndRaise('Missing info required to delete fencer')
    d = str(d)
 
    query = "delete from fencers where fencer_id = %s"
    cursor.execute(query, (d,))
    cnx.commit()
    print "<h2>Fencer with ID %s has been removed from the match.</h2>" % d
 
if form.getvalue('update'):
    u = form.getvalue('update')
    c = form.getvalue('column')
    s = form.getvalue('set')
    if None in (u,c,s):
        printAndRaise('Missing info required to update fencer')
    u = str(u)
    c = str(c)
    s = str(s)
 
    if c not in columns:
        printAndRaise('Column submitted is not a column in fencers')
        
    query = "update fencers set " + c + "= %s where fencer_id = %s"
    cursor.execute(query, (s,u))
    cnx.commit()
    print "<h2>%s for Fencer with ID %s has been updated to %s.</h2>" % (c, u, s)
    
if form.getvalue('id'):
    i = form.getvalue('id')
    n = form.getvalue('name')
    t = form.getvalue('team')
    sq = form.getvalue('squad')
    if None in (i,n,t,sq):
        printAndRaise('Missing info required to insert new fencer')
    i = str(i)
    n = str(n)
    t = str(t)
    sq = str(sq)
    query = "select * from fencers where fencer_id = %s"
    cursor.execute(query,(i,))
    result = cursor.fetchall()
    if len(result) != 0:
        printAndRaise('Fencer with this ID already exists')
    query = "insert into fencers values (%s, %s, 0,0,0,0)"
    cursor.execute(query, (i,n))
    query = "insert into team_members values (%s, %s, %s)"
    cursor.execute(query, (t,i,sq))
    cnx.commit()
    print "<h2>Fencer %s with ID %s has been added to the match.</h2>" % (n,i)
 
if form.getvalue('attr'):
    a = form.getvalue('attr')
    f = form.getvalue('fencer')
    if None in (a,f):
        printAndRaise('Missing info required to display fencers')
    if str(a)[0] == "[":
        aStr = ""
        for val in a:
            aStr += val + ", "
        a = aStr[:-2]
        
    if str(f)[0] == "[":
        fStr = ()
        for val in f:
            fStr = fStr + (str(val),)
        f = fStr
        tup = 1
    else:
        f = str(f)
 
    l = 1
    if tup:
        l = len(f)
        b = a.split(", ")
        for at in b:
            if at not in columns:
               printAndRaise('Column submitted is not a column in fencers')
    else:
        if a not in columns:
            printAndRaise('Column submitted is not a column in fencers')
    query = "select " + a + " from fencers where fencer_id in (" + ("%s, " * l)
    query = query[:-2] + ")"
    if tup:
        cursor.execute(query, f)
    else:
        cursor.execute(query, (f,))
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
 