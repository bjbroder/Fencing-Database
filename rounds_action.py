#!/usr/bin/python                                                                              \
                                                                                                
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
   cnx = mysql.connector.connect(user='bbroder', password='dbkey', host='localhost', database='\
bbroder1')
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

try:
cursor.execute("show columns from rounds")
except mysql.connector.Error as e:
    print "Error:", str(e)
columns = {str(col[0]) for col in cursor.fetchall()}

if form.getvalue('delete'):
    d = form.getvalue('delete')
    print d
    if d == None:
        printAndRaise('Missing info required to delete match')
    d = str(d).split('&')
    print d
    query = "delete from rounds where round_number = %s and match_id = %s"
    try:
        cursor.execute(query, (d[0],d[1]))
        cnx.commit()
        print "<h2>Match has been removed.</h2>"
    except mysql.connector.Error as e:
        print "Error:", str(e)

if form.getvalue('update'):
    u = form.getvalue('update')
    c = form.getvalue('column')
    s = form.getvalue('set')
    if None in (u,c,s):
        printAndRaise('Missing info required to update fencer')
    u = str(u).split('&')
    c = str(c)
    s = str(s)

    if c not in columns:
        printAndRaise('Column submitted is not a column in rounds')

    query = "update rounds set " + c + "= %s where round_number = %s and match_id = %s and team\
_id = %s"
    #^this is bad for consistency - fix!                                                        
    try:
        cursor.execute(query, (s,u[0],u[1], u[2]))
        cnx.commit()
        print "<h2>Match has been updated.</h2>"
    except mysql.connector.Error as e:
        print "Error:", str(e)

if form.getvalue('round'):
    r = form.getvalue('round')
    m = form.getvalue('match')
    tA = form.getvalue('teamA')
    tB = form.getvalue('teamB')
    if None in (r,m,tA,tB):
        printAndRaise('Missing info required to insert new match')
    r = str(r)
    m = str(m)
    tA = str(tA)
    tB = str(tB)
    if tA == tB:
        printAndRaise('A team cannot play against itself')
    query = "select * from rounds where match_id = %s"
    try:
        cursor.execute(query,(m,))
    except mysql.connector.Error as e:
        print "Error:", str(e)
    result = cursor.fetchall()
    if len(result) != 0:
        printAndRaise('Match with this ID already exists')
    query = "select * from rounds where team_id = %s and round_number = %s"
    try:
        cursor.execute(query,(tA,r))
    except mysql.connector.Error as e:
        print "Error:", str(e)
    result = cursor.fetchall()
    if len(result) != 0:
        printAndRaise('Team A is busy during this round')
    try:
        cursor.execute(query,(tB,r))
    except mysql.connector.Error as e:
        print "Error:", str(e)
    result = cursor.fetchall()
    if len(result) != 0:
        printAndRaise('Team B is busy during this round')
    query = "insert into rounds values (%s, %s, 'A', %s)"
    try:
        cursor.execute(query, (tA,r,m))
        query = "insert into rounds values (%s, %s, 'B', %s)"
        cursor.execute(query, (tB,r,m))
        cnx.commit()
    except mysql.connector.Error as e:
        print "Error:", str(e)
    print "<h2>Match has been added.</h2>"

if form.getvalue('attr'):
    a = form.getvalue('attr')
    mat = form.getvalue('matches')
    if None in (a,mat):
        printAndRaise('Missing info required to display matches')
    if str(mat)[0] == "[":
        matStr = ()
        for val in mat:
            matStr = matStr + (str(val),)
        mat = matStr
        tup = 1
        l = len(mat)
    else:
        f = str(mat)
        l = 1

    if str(a)[0] == "[":
        aStr = ""
        for val in a:
            aStr += val + ", "
        a = aStr[:-2]

        if tup:
            l = len(mat)
            b = a.split(", ")
            for at in b:
                if at not in columns:
                    printAndRaise('Column submitted is not a column in matches')
        
    else:
        if a not in columns:
            printAndRaise('Column submitted is not a column in matches')
    query = "select " + a + " from rounds where match_id in (" + ("%s, " * l)
    query = query[:-2] + ")"
    if tup:
        try:
            cursor.execute(query, mat)
        except mysql.connector.Error as e:
            print "Error:", str(e)
    else:
        try:
            cursor.execute(query, (mat,))
        except mysql.connector.Error as e:
            print "Error:", str(e)
    print "Data returned from columns " + a + ":"
    for res in cursor:
        print "<br>"
        if type(res) == type(()):
            print "|"
            for r in res:
                print r
                print "|"


print '<br><br>'
print '<form action="http://ada.sterncs.net/~bbroder/fencing.html">'
print '<button type="submit">Home</button>'
print '</form>'

print '<form action="http://ada.sterncs.net/~bbroder/cgi-bin/roundsForm.py">'
print '<button type="submit">Back</button>'
print '</form>'
        
print "</body>"
print "</html>"

cursor.close()
cnx.close()
                
