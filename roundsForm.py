#!/usr/bin/python                                                                                           

import mysql.connector

cnx = mysql.connector.connect(user='bbroder', password='dbkey', host='localhost', database='bbroder1')

cursor = cnx.cursor()

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '</head>'
print '<body>'

#DELETE                                                                                                     
try:
    cursor.execute("select bout_id, match_id, squad from round_bouts")
except mysql.connector.Error as e:
    print "Error:", str(e)
print 'Which bout would you like to delete?'
print '<form action = "/~bbroder/cgi-bin/roundbouts_action.py" method = "post">'
print '<select name = "delete">'
for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0] + ', ' + row[1] + ', ' + row[2]
print '</select>'
print '<br><input type = "submit" value = "Submit" />'
print '</form>'

print '<p>'
print '*****'
print '</p>'

#UPDATE                                                                                                     
try:
    cursor.execute("select bout_id from round_bouts")
except mysql.connector.Error as e:
        print "Error:", str(e)
print 'Which bout would you like to update?'
print '<form action = "/~bbroder/cgi-bin/roundbouts_action.py" method = "post">'
print '<select name = "update">'
for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0]
print '</select>'

cursor.execute("show columns from round_bouts")
print '<br>'
print 'Which attribute of this bout would you like to update?'
print '<select name = "column">'
for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0]
print '</select>'
print '<br>New Value: <input type = "text" name = "set">  <br />'
print '<br><input type = "submit" value = "Submit" />'
print '</form>'

print '<p>'
print '*****'
print '</p>'

#INSERT                                                                                                     
print 'New Bout to Insert:'
print '<form action = "/~bbroder/cgi-bin/roundbouts_action.py" method = "post">'
print 'Bout ID: <input type = "text" name = "bout_id">  <br />'
print 'Match ID: <input type = "text" name = "match_id">  <br />'
print 'Squad: <input type = "text" name = "squad">  <br />'
print 'Fencer IDs for Team A:<br>'
print '1: <input type = "text" name = "f1a">  <br />'
print '2: <input type = "text" name = "f2a">  <br />'
print '3: <input type = "text" name = "f3a">  <br />'
print '<br>'
print 'Fencer IDs for Team B:<br>'
print '1: <input type = "text" name = "f1b">  <br />'
print '2: <input type = "text" name = "f2b">  <br />'
print '3: <input type = "text" name = "f3b">  <br />'
print '<input type = "submit" value = "Submit" />'
print '</form>'

print '<p>'
print '*****'
print '</p>'

#SELECT                                                                                                     
print '<form action = "/~bbroder/cgi-bin/roundbouts_action.py" method = "POST">'
try:
    cursor.execute("show columns from round_bouts")
except mysql.connector.Error as e:
        print "Error:", str(e)
print 'Columns to be displayed:'
print '<br>'
print '<select name = "attr", multiple>'
for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0] + '</option>'
print '</select>'

print '<br>'
print 'Bouts to be displayed:'
print '<br>'
try:
    cursor.execute("select bout_id from round_bouts")
except mysql.connector.Error as e:
        print "Error:", str(e)

print '<select name = "bout", multiple>'                                                                   \

for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0] + '</option>'
print '</select>'

print '<br><input type = "submit" value = "Submit" />'
print '</form>'

print '<form action="http://ada.sterncs.net/~bbroder/fencing.html">'
print '<button type="submit">Home</button>'
print '</form>'

print '</body>'
print '</html>'

cursor.close()
cnx.close()

