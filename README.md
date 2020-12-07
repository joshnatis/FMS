# food_db
Food Management System (CS 435)

## Setup
These are directions to:
1. install MariaDB (a free and open source version of MySQL) on Arch Linux,
2. create a user in mariadb,
3. assign them a database,
4. create tables and fill the database with our data
```bash
$ sudo pacman -Syu mariadb
$ sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
$ cd '/usr' ; /usr/bin/mysqld_safe --datadir='/var/lib/mysql'   # might not be necessary
$ sudo systemctl enable mariadb.service
$ sudo systemctl start mariadb.service
$ mysql_secure_installation   # select 'y' for all options
$ reboot
$ su root
$ mysql -u root -p
```
```sql
mariadb> CREATE USER josh@localhost IDENTIFIED BY 'password';
mariadb> CREATE DATABASE food_db;
mariadb> GRANT ALL PRIVILEGES ON food_db.* TO 'josh'@'localhost';
mariadb> exit   # bye
```
```bash
$ su josh
$ cd ~ && https://github.com/joshnatis/food_db/
$ mysql -u josh -p
```
```sql
mariadb> USE food_db;
mariadb> source /home/josh/food_db/documentation/load.sql
mariadb> source /home/josh/food_db/documentation/useful_queries.sql
mariadb> exit   # bye
```
### Manually Controlling MariaDB
Because we ran `systemctl enable mariadb.service`, the MariaDB server will always be running in the background on our computer (and will start automatically upon booting our computer). This is normal for production environments, but at home we don't need the extra process running constantly if we're not using it. We can instead start and stop MariaDB manually:
```bash
# run this once, to disable it from starting at boot
$ sudo systemctl disable mariadb.service

# commands to manually start/stop:
$ sudo systemctl start mariadb.service
$ sudo systemctl stop mariadb.service

# NOTE: if you try to log in to MariaDB with the server still stopped, you'll get the following error:
# ERROR 2002 (HY000): Can't connct to local MySQL server ...

# You check whether the server is up by running:
ps -A | grep "maria" # if the output is empty, it's stopped
```
---
## Connecting MySQL to Python
```bash
$ pip install mysql-connector-python
```
Here's a minimal example of connecting to and querying a database with the connector:
```python
import mysql.connector

#======================#
# CONNECT THE DATABASE #
#======================#

config = {
  'user':'josh',
  'password':'yourpassword',
  'host':'localhost',
  'database':'food_db',
  'charset':'utf8'
}

try:
  cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
  print(err)
  exit(1)

#======================#
#  QUERY THE DATABASE  #
#======================#
cursor = cnx.cursor()

query = ("SELECT food_id, food_name FROM food_types WHERE calories < %s LIMIT %s")
max_cals = 500
lim = 20

cursor.execute(query, (max_cals, lim))  # replaces '%s' with max_cals and lim, respectively

#=========================#
# ACCESS THE QUERIED INFO #
#=========================#

for (fid, name) in cursor:
  print("ID:", fid, "NAME:", name)

cursor.close()
cnx.close()
```
### Securely-ish Entering Your Password
It's probably not a good idea to hardcode our password into our Python program if we're going to be sharing it with others. Here's one method to get around that:
```bash
$ export MARIADB_PASSWORD="yourpassword"
```
```python
import os
password = os.environ.get("MARIADB_PASSWORD")
```

---

[Link to Presentation](https://docs.google.com/presentation/d/1YkzTePw4BZuKCEPLfe2GVGyBCsglpgu4ILT1aibKvCc/edit?usp=sharing)
