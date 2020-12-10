#============================================================================#
# Title        : Food Management System Database Querier                     #
# Author       : Josh Natis                                                  #
# Description  : This program receives queries from a client (either the CLI #
#                or a keyboard, if run directly), sends them to the database #
#                , and transmits the data back formatted as a table.         #
# Repository   : https://github.com/joshnatis/FMS                            #
# License      : MIT                                                         #
# Usage                                                                      #
#    As a standalone program:                                                #
#       python3 food_db.py                                                   #
#       Note: queries are not sanitized; all your base are belong to us      #
#       To be fair, you need to log in to the database before querying,      #
#       and if you can do that the data was PWNED anyways.                   #
#                                                                            #
#   As an imported module:                                                   #
#      (1) Call login() with the proper credentials                          #
#      (2) Call getdata(), passing in the parameters to your query as a      #
#          dictionary. Note that this getdata() function is tailored         #
#          specifically to our database and CLI (it expects the parameters   #
#          "category", "client", "subject", and "order", with specific       #
#          values for each). To make general purpose queries, this auxillary #
#          function is not necessary -- simply pass your query string into   #
#          a call to cursor.execute(), and then pass the cursor into the     #
#          tabulate() function if you want to tabulate the data.             #
#============================================================================#

import os
import tabulator
import mysql.connector

cnx = None
cursor = None

def login(username, password):
	config = {
		'user':username,
		'password':password,
		'host':'localhost',
		'database':'food_db',
		'charset':'utf8'
	}
	global cnx, cursor
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()

def getusers():
	cursor.execute('SELECT user_name FROM users')
	return [user[0] for user in cursor]

def getuserid(username):
	query = 'SELECT user_id FROM users WHERE user_name="' + username + '"'
	cursor.execute(query)
	return str(cursor.fetchone()[0])

def buildquery(query_params):
	category = query_params["category"]
	client = query_params["client"]
	subject = query_params["subject"]

	user_id = getuserid(client) if client != "Household" else None

	QUERY_TABLE = {
		"items" : """SELECT [1] SUBSTR(food_types.food_name, 1, 30) AS food,
		             food_instances.quantity AS num, CONCAT("$", FORMAT(
		             food_instances.total_price, 2)) as total, IF(DATEDIFF(
		             food_instances.expiration_date, CURDATE()) < 0, "expired", CONCAT(
		             DATEDIFF(food_instances.expiration_date, CURDATE()), " days")) AS
		             expiring, SUBSTR(stores.store_name, 1, 20) AS store,
		             food_instances.purchase_date AS purchased FROM food_instances JOIN
		             users ON (users.user_id = food_instances.user_id) JOIN food_types ON
		             (food_types.food_id = food_instances.food_id) JOIN stores ON
		             (stores.store_id = food_instances.food_id) [2] ORDER BY
		             food_instances.[3];""",

		"quantities" : """SELECT food_types.food_name, COUNT(food_instances.food_id)
		                      * food_instances.quantity as num_purchases FROM food_types
		                      JOIN food_instances ON (food_types.food_id = food_instances.food_id)
		                      [1] GROUP BY food_types.food_id, food_instances.quantity ORDER BY
		                      num_purchases""",

		"money" : """SELECT CONCAT("$", FORMAT(SUM(total_price),2)) AS total_spent FROM
		             food_instances [1]""",

		"%healthy" : """SELECT CONCAT(FORMAT(percentage_of_healthy_items,2),"%") AS
		                percentage_of_healthy_items FROM (SELECT (100 * (SELECT COUNT(*) AS
		                num_healthy_items from( SELECT COUNT(food_instances.food_id) AS
		                num_purchases, food_types.health_scale FROM food_types JOIN
		                food_instances ON (food_types.food_id = food_instances.food_id)
		                WHERE food_types.health_scale >= 7 AND user_id IS NOT NULL GROUP BY
		                food_types.food_id, food_types.health_scale ORDER BY num_purchases)
		                AS c) / (SELECT COUNT(*) AS total_items from( SELECT
		                COUNT(food_instances.food_id) as num_purchases, food_types.health_scale
		                FROM food_types JOIN food_instances ON (food_types.food_id =
		                food_instances.food_id) WHERE user_id IS NOT NULL GROUP BY
		                food_types.food_id, food_types.health_scale ORDER BY num_purchases)
		                AS a )) AS percentage_of_healthy_items) AS w; """,
	}

	query = QUERY_TABLE[subject]

	if subject == "items":
		if client == "Household": query = query.replace("[1]", "users.user_name AS user,")
		else: query = query.replace("[1]", "")

		if category == "History":
			if client == "Household": query = query.replace("[2]", "")
			else:
				query = query.replace("[2]", "WHERE food_instances.user_id=" + user_id)
		else:
			if client == "Household":
				query = query.replace("[2]", "WHERE available=True")
			else:
				query = query.replace("[2]", "WHERE food_instances.user_id=" + user_id + " AND available=True")

		query = query.replace("[3]", query_params["order"])

	elif subject == "quantities" or subject == "money":
		time_period = query_params["time_period"]
		constraint = "purchase_date >= SUBDATE(CURDATE(), "

		if time_period == "Time": constraint = ""
		else: constraint += "INTERVAL 1 " + time_period.upper() + ")"

		if client != "Household":
			if time_period != "Time": constraint += " AND "
			constraint += "user_id=" + user_id

		if category == "Currently":
			if time_period != "Time" or client != "Household": constraint += " AND "
			constraint += "available=True"

		if constraint != "": constraint = "WHERE " + constraint
		query = query.replace("[1]", constraint)
		if subject == "quantities": query += " " + query_params["order"]

	elif subject == "%healthy":
		if category == "History" and client != "Household":
			query = query.replace("IS NOT NULL", "=" + user_id)
		elif category == "Currently":
			if client == "Household":
				query = query.replace("IS NOT NULL", "IS NOT NULL AND available=True")
			else:
				query = query.replace("IS NOT NULL", "=" + user_id + " AND available=True")

	return query

def getdata(query_params):
	query = buildquery(query_params)
	cursor.execute(query)
	data = tabulate(cursor).split("\n")
	title = query_params["client"] + "'s " + query_params["subject"] + ":"
	data.insert(0, title)
	return data

def tabulate(data):
	df = []
	df.append([" " + col.strip() + " " for col in data.column_names])
	for row in data:
		columns = [(" " + str(col).strip() + " ") for col in row]
		df.append(columns)
	tabulator.pad_missing_columns(df)
	return tabulator.print_table(df)

def main():
	import getpass
	username, password = input("Username: "), getpass.getpass("Password: ")
	config = {
		'user':username,
		'password':password,
		'host':'localhost',
		'database':'food_db',
		'charset':'utf8'
	}
	try:
		cnx = mysql.connector.connect(**config)
	except mysql.connector.Error as err:
		print(err)
		exit()

	cursor = cnx.cursor()

	print("You may begin querying.")
	cont = True
	while cont:
		query = (input("% "))
		cursor.execute(query)
		print(tabulate(cursor), end="")
		cont = input("\nContinue? (y/n): ") == "y"

	cursor.close()
	cnx.close()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Bye")

