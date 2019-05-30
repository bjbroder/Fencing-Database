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
 
d = u = c = s = 0
b_id = m_id = sq = f1a = f2a = f3a = f1b = f2b = f3b = 0
a = b = tup = 0
 
cursor.execute("show columns from round_bouts")
columns = {str(col[0]) for col in cursor.fetchall()}
 
if form.getvalue('delete'):
    d = form.getvalue('delete')
    if d == None:
        printAndRaise('Missing info required to delete bout')
    d = str(d)
 
    query = "delete from round_bouts where bout_id = %s"
    cursor.execute(query, (d,))
    cnx.commit()
    print "<h2>Bout with ID %s has been removed from the match.</h2>" % d
 
if form.getvalue('update'):
    u = form.getvalue('update')
    c = form.getvalue('column')
    s = form.getvalue('set')
    if None in (u,c,s):
        printAndRaise('Missing info required to update bout')
    u = str(u)
    c = str(c)
    s = str(s)
 
    if c not in columns:
        printAndRaise('Column submitted is not a column in round_bouts')
        
    query = "update round_bouts set " + c + "= %s where bout_id = %s"
    cursor.execute(query, (s,u))
    cnx.commit()
    print "<h2>%s for bout with ID %s has been updated to %s.</h2>" % (c, u, s)
    
if form.getvalue('b_id'):
    b_id = form.getvalue('b_id')
    m_id = form.getvalue('m_id')
    sq = form.getvalue('squad')

    f1a = form.getvalue(‘f1a’)
    f2a = form.getvalue(‘f2a’)
    f3a = form.getvalue(‘f3a’)
    f1b = form.getvalue(‘f1b’)
    f2b = form.getvalue(‘f2b’)
    f3b = form.getvalue(‘f3b’)

    if None in (b_id,m_id,sq):
        printAndRaise('Missing info required to insert new bout')
    b_id = str(b_id)
    m_id = str(m_id)
    sq = str(sq)
    query = "select * from bouts where bout_id = %s"
    cursor.execute(query,(i,))
    result = cursor.fetchall()
    if len(result) != 0:
        printAndRaise('Bout with this ID already exists')
    query = "insert into round_bouts values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (b_id, m_id, sq, f1a, f2a, f3a, f1b, f2b, f3b))
    cnx.commit()
    print "<h2>Bout with ID %s has been added to the match.</h2>" % (b_id)
 
if form.getvalue('attr'):
    a = form.getvalue('attr')
    b = form.getvalue('bout')
    if None in (a,b):
        printAndRaise('Missing info required to display bouts')
    if str(a)[0] == "[":
        aStr = ""
        for val in a:
            aStr += val + ", "
        a = aStr[:-2]
        
    if str(b)[0] == "[":
        bStr = ()
        for val in b:
            bStr = bStr + (str(val),)
        b = bStr
        tup = 1
    else:
        b = str(b)
 
    l = 1
    if tup:
        l = len(b)
        aSplit = a.split(", ")
        for at in aSplit:
            if at not in columns:
               printAndRaise('Column submitted is not a column in bouts')
    else:
        if a not in columns:
            printAndRaise('Column submitted is not a column in bouts')
    query = "select " + a + " from bouts where bout_id in (" + ("%s, " * l)
    query = query[:-2] + ")"
    if tup:
        cursor.execute(query, b)
    else:
        cursor.execute(query, (b,))
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
 