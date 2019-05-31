# Fencing-Database

Problem: At any given fencing meet, there is a lot of data to organize - each participating team (often around 10 teams at a meet) has 3 squads which each have around 3 players (although there can be missing teammates or substitutions if there are extra players available). Each squad on each team has three rounds of 3 bouts against the corresponding squad on every other school’s team. These bouts should all happen in the fewest number of rounds, meaning that it is important to maximize the number of schools competing one-on-one at a given time. Right now, all of this organization is done by hand which is both time-consuming and error-prone. By using a database system, the scheduling required for a fencing meet can be drastically improved and will save a lot of time and paper.

Solution: I initially created five tables to represent the teams (“teams”), the fencers (“fencers”), the teams that sparred each other each round (“rounds”), and the bouts that occurred in each round (“round_bouts”). While most of this structure stayed the same throughout, I noticed that there was a lot of duplicate information being stored in “round_bouts” so I redesigned the table to have columns to have a bout_id, a match_id (that exists in the “rounds” table), and the three fencers (using their fencer id from “fencers”) that would play for each side. As the table currently stands, I am not able to set the match_id as a foreign key since the value is not unique in the rounds table. To “fake” the match_id being a foreign key, my cgi scripts are coded to check that the match_id exist before adding a row to “round_bouts.” In the future, I would perhaps like to reformat the “rounds” table so that match_id is used uniquely and can therefore be used by “round_bouts” as a foreign key. The reason why this was not done to begin with is because the current format makes it easier to see which teams are playing in a given round (the other format would split the playing teams into two separate columns - TeamA and TeamB). Depending on how the database is used, however, having this foreign key constraint may prove to be more valuable than the ease of getting the ID’s of the playing teams.

ER Diagram: https://docs.google.com/document/d/1S8E8k4LZNlkNwYZKBblnuJBTJUrA0FnPn_-MlJ4_iqA/edit?usp=sharing
