!/usr/bin/python                                                                                           

import mysql.connector

cnx = mysql.connector.connect(user='bbroder', password='dbkey', host='localhost', database='bbroder1')

cursor = cnx.cursor()

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '</head>'
print '<body>'

#DELETE                                                                                                     
cursor.execute("select distinct round_number, match_id from rounds")
results = cursor.fetchall()
r0 = []
r1 = []
teamRes = []
for res in results:
    rn = str(res[0])
    r0.append(rn)
    mi = str(res[1])
    r1.append(mi)
    cursor.execute("select team_id from rounds where round_number = %s and match_id = %s", (rn,mi))
    tr = cursor.fetchall()
    trString = []
    for e in tr:
        trString.append(str(e)[3:-3])
    teamRes.append(trString)


matchesInRound = zip(r0, r1, teamRes)
mir = []
for i in matchesInRound:
    mir.append(str(i))
print 'Which match would you like to delete?'
print '<br>Round | Match ID | Teams Playing'
print '<form action = "/~bbroder/cgi-bin/rounds_action.py" method = "post">'
print '<select name = "delete">'
for row in matchesInRound:
   r = str(row[0]) + ', ' + str(row[1]) + ', ' + str(row[2])
    print '<option value = ' + row[0] + '&' + row[1]  + ' >' + r
print '</select>'
print '<br><input type = "submit" value = "Submit" />'
print '</form>'

print '<p>'
print '*****'
print '</p>'

#UPDATE                                                                                                     
cursor.execute("select round_number, match_id, team_id from rounds")
results = cursor.fetchall()
print 'Which match would you like to update?'
print '<br>Round | Match ID | Team'
print '<form action = "/~bbroder/cgi-bin/rounds_action.py" method = "post">'
print '<select name = "update">'
for row in results:
    r = str(row[0]) + ', ' + str(row[1]) + ', ' + str(row[2])
    print '<option value = ' + str(row[0]) + '&' + str(row[1]) + '&' + str(row[2]) + ' >' + r
print '</select>'

cursor.execute("show columns from rounds")
print '<br>'
print 'Which column of rounds would you like to update?'
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
print 'New Match to Insert:'
print '<form action = "/~bbroder/cgi-bin/rounds_action.py" method = "post">'
print 'Round: <input type = "text" name = "round">  <br />'
print 'Match_ID: <input type = "text" name = "match">  <br />'
cursor.execute("select team_id, team_name from teams")
print 'Team A: '
print '<select name = "teamA">'
result = cursor.fetchall()
for row in result:
    print '<option value = ' + row[0] + ' >' + row[0] + ', ' + row[1]
print '</select>'
print 'Team B: '
print '<select name = "teamB">'
for row in result:
    print '<option value = ' + row[0] + ' >' + row[0] + ', ' + row[1]
print '</select>'
print '<input type = "submit" value = "Submit" />'
print '</form>'

print '<p>'
print '*****'
print '</p>'

#SELECT                                                                                                     
print '<form action = "/~bbroder/cgi-bin/rounds_action.py" method = "POST">'
cursor.execute("show columns from rounds")
print 'Columns to be displayed:'
print '<br>'

print '<select name = "attr", multiple>'
for row in cursor:
    print '<option value = ' + row[0] + ' >' + row[0] + '</option>'
print '</select>'

print '<br>'
print 'Matches to be displayed:'
print '<br>Match ID | Team'
print '<br>'
cursor.execute("select match_id, team_id from rounds")

print '<select name = "matches", multiple>'
for row in cursor:
    print '<option value = ' + str(row[0]) + ' >' + str(row[0]) + ', ' + str(row[1]) + '</option>'
print '</select>'

print '<br><input type = "submit" value = "Submit" />'
print '</form>'
print '</body>'
print '</html>'

cursor.close()
cnx.close()
