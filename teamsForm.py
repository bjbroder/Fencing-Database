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
cursor.execute("select team_id, team_name from teams")
print 'Which team would you like to delete?'
print '<form action = "/~bbroder/cgi-bin/teams_action.py" method = "post">'
print '<select name = "delete">'
for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0] + ', ' + row[1]
print '</select>'
print '<br><input type = "submit" value = "Submit" />'
print '</form>'

print '<p>'
print '*****'
print '</p>'

#UPDATE                                                                                                  
cursor.execute("select team_id, team_name from teams")
print 'Which team would you like to update?'
print '<form action = "/~bbroder/cgi-bin/teams_action.py" method = "post">'
print '<select name = "update">'
for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0] + ', ' + row[1]                                   \

print '</select>'

cursor.execute("show columns from teams")
print '<br>'
print 'Which column of teams would you like to update?'
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

#SELECT                                                                                                  
print '<form action = "/~bbroder/cgi-bin/teams_action.py" method = "POST">'
cursor.execute("show columns from teams")
print 'Columns to be displayed:'
print '<br>'

print '<select name = "attr", multiple>'
for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0] + '</option>'
print '</select>'

print '<br>'
print 'Teams to be displayed:'
print '<br>'
cursor.execute("select team_id, team_name from teams")

print '<select name = "team", multiple>'                                                                \

for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0] + ', ' + row[1] + '</option>'
print '</select>'

print '<br><input type = "submit" value = "Submit" />'
print '</form>'
print '</body>'
print '</html>'

cursor.close()
cnx.close()
