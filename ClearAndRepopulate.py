#!/usr/bin/python                                                                                                                                                                    
import mysql.connector
cnx = mysql.connector.connect(user='bbroder', password='dbkey', host='localhost', database='bbroder1\                                                                                
')
cursor = cnx.cursor()

query = "drop tables round_bouts, rounds, team_members, fencers, teams"
cursor.execute(query)

query = "create table teams (team_id varchar(10) not null, team_name varchar(30) not null, sabre_points int(3), epee_points int(3), foil_points int(3), primary key (team_id))"
cursor.execute(query)

query = "create table rounds (team_id varchar(10) not null, round_number int(2) not null, team_side varchar(1) not null check (team_side in ('A', 'B')), match_id varchar(10) not nu\
ll, primary key (team_id, round_number), foreign key (team_id) references teams (team_id) on delete cascade)"
cursor.execute(query)

query = "create table fencers (fencer_id varchar(10) not null, fencer_name varchar(30) not null, num_victories int(2), num_losses int(2), touches_scored int(3), touches_received in\
t(3), primary key (fencer_id))"
cursor.execute(query)

query = "create table team_members (team_id varchar(10) not null, fencer_id varchar(10) not null, squad varchar(5) not null check (squad in ('sabre','epee','foil')), primary key (t\
eam_id, fencer_id), foreign key (team_id) references teams (team_id) on delete cascade, foreign key (fencer_id) references fencers (fencer_id) on delete cascade)"
cursor.execute(query)

query = "create table round_bouts (match_id varchar(10) not null, team_side varchar(1) not null check (team_side in ('A', 'B')), squad varchar(5) not null check (squad in ('sabre',\
'epee','foil')), player1_ID varchar(10),  player2_ID varchar(10), player3_ID varchar(10), primary key (match_id, team_side, squad))"
#    -> foreign key (match_id, team_side) references rounds (match_id, team_side),                                                                                                   
#    -> foreign key (squad) references team_members (squad));                                                                                                                        
#Got an error with the foreign keys will add them later as written here                                                                                                              
cursor.execute(query)

query = "insert into teams values (101, 'Lions', 0, 0, 0), (102, 'Tigers', 0, 0, 0), (103, 'Bears', 0, 0, 0), (104, 'OhMy', 0, 0, 0)"
cursor.execute(query)

query = "insert into fencers values (201, 'Lily', 0, 0, 0, 0), (202, 'Lauren', 0, 0, 0, 0), (203, 'Lucy', 0, 0, 0, 0), (204, 'Leah', 0, 0, 0, 0), (205, 'Layla', 0, 0, 0, 0), (206, \
'Lydia', 0, 0, 0, 0), (207, 'Libby', 0, 0, 0, 0), (208, 'Lisa', 0, 0, 0, 0),(209, 'Lara', 0, 0, 0, 0),(211, 'Tabetha', 0, 0, 0, 0),(212, 'Tamsen', 0, 0, 0, 0),(213, 'Tali', 0, 0, 0\
, 0),(214, 'Taylor', 0, 0, 0, 0),(215, 'Talya', 0, 0, 0, 0),(216, 'Tasha', 0, 0, 0, 0),(217, 'Tarra', 0, 0, 0, 0),(218, 'Tasmin', 0, 0, 0, 0),(219, 'Tillie', 0, 0, 0, 0),(221,'Bay\
', 0, 0, 0, 0),(222, 'Bella', 0, 0, 0, 0),(223, 'Bria', 0, 0, 0, 0),(224, 'Brynn', 0, 0, 0, 0),(225, 'Brooke', 0, 0, 0, 0),(226, 'Bobby', 0, 0, 0, 0),(227, 'Brenda', 0, 0, 0, 0),(2\
28, 'Betty', 0, 0, 0, 0),(229, 'Blessing', 0, 0, 0, 0),(231, 'Olga', 0, 0, 0, 0),(232, 'Olivia', 0, 0, 0, 0),(233, 'Orit', 0, 0, 0, 0),(234, 'Orly', 0, 0, 0, 0),(235, 'Opal', 0, 0,\
 0, 0),(236, 'Olympia', 0, 0, 0, 0),(237, 'Octavia', 0, 0, 0, 0),(238, 'Onyx', 0, 0, 0, 0),(239, 'Ora', 0, 0, 0, 0)"
cursor.execute(query)

query = "insert into team_members values(101, 201, 'Sabre'),(101, 202, 'Sabre'),(101, 203, 'Sabre'),(101, 204, 'Epee'),(101, 205, 'Epee'),(101, 206, 'Epee'),(101, 207, 'Foil'),(101\
, 208, 'Foil'),(101, 209, 'Foil'), (102, 211, 'Sabre'),(102, 212, 'Sabre'), (102, 213, 'Sabre'),(102, 214, 'Epee'), (102, 215, 'Epee'),(102, 216, 'Epee'), (102, 217, 'Foil'),(102, \
218, 'Foil'),(102, 219, 'Foil'),(103, 221, 'Sabre'),(103, 222, 'Sabre'),(103, 223, 'Sabre'), (103, 224, 'Epee'),(103, 225, 'Epee'), (103, 226, 'Epee'),(103, 227, 'Foil'), (103, 228\
, 'Foil'),(103, 229, 'Foil'), (104, 231, 'Sabre'),(104, 232, 'Sabre'),(104, 233, 'Sabre'),(104, 234, 'Epee'), (104, 235, 'Epee'),(104, 236, 'Epee'),(104, 237, 'Foil'),(104, 238, 'F\
oil'), (104, 239, 'Foil')"
cursor.execute(query)

query = "insert into rounds values (101, 1, 'A', 301),(102, 1, 'B', 301), (103, 1, 'A', 302),(104, 1, 'B', 302),(104, 2, 'A', 303),(101, 2, 'B', 303), (102, 2, 'A', 304),(103, 2, '\
B', 304), (102, 3, 'A', 305),(104, 3, 'B', 305), (101, 3, 'A', 306),(103, 3, 'B', 306)"
cursor.execute(query)

query = "insert into round_bouts values (301, 'A', 'Sabre', 201, 202, 203),(303, 'B', 'Sabre', 202, 203, 201),(3\
06, 'A', 'Sabre', 203, 201, 202),(301, 'A', 'Epee', 204, 205, 206), (303, 'B', 'Epee', 205, 206, 204),(306, 'A',\
 'Epee', 206, 204, 205), (301, 'A', 'Foil', 207, 208, 209),(303, 'B', 'Foil', 208, 209, 207), (306, 'A', 'Foil',\
 209, 207, 208),(301, 'B', 'Sabre', 211, 212, 213), (304, 'A', 'Sabre', 212, 213, 211),(305, 'A', 'Sabre', 213, \
211, 212),(301, 'B', 'Epee', 214, 215, 216),(304, 'A', 'Epee', 215, 216, 214),(305, 'A', 'Epee', 216, 214, 215),\
(301, 'B', 'Foil', 217, 218, 219), (304, 'A', 'Foil', 218, 219, 217),(305, 'A', 'Foil', 219, 217, 218),(302, 'A'\
, 'Sabre', 221, 222, 223),(304, 'B', 'Sabre', 222, 223, 221),(306, 'B', 'Sabre', 223, 221, 222)"
#Need to finish putting in values                                                                                
cursor.execute(query)

cnx.commit()
cursor.close()
