# Food Management System

By [Josh](https://github.com/joshnatis), [Liulan](https://github.com/liulanz), and [Chi Shing](https://github.com/chislee0708) for CS435

```
Understanding our relationship with food can have many benefits.
However, it is quite difficult to track one’s food-related activities manually.
Writing down every item we buy along with its price, expiration  date, and so on
all while keeping this information safe and organized over long periods of time
requires a herculean effort. Yet, this information is immensely useful to analyze,
as it can help us spend smarter, eat healthier, and be less wasteful. Our system
will allow users to programmatically track food items.
```
`Click me to watch a demo!`
<br>
<a href="https://youtu.be/_mlEGVKiPXE">
  <img src="https://raw.githubusercontent.com/joshnatis/assets/master/FMS/food_db_cli_preview.png?token=AHP5EJSXQXIEF45HAEL4ZKS73P32C" alt="vid preview" width="50%" height="50%">
</a>

## Usage
```bash
# Make sure you have an active MySQL or MariaDB server running,
# and that it has a database named 'food_db' filled with our data,
# as well as a user account that has access to the database.
# See the 'Setup' section for information on how to do that.

$ python3 food_cli.py
```

## Install
```bash
$ pip3 install mysql-connector-python
$ git clone https://github.com/joshnatis/fms
```
---

## Setup
These are directions to:
1. install MariaDB (a free and open source version of MySQL) on Arch Linux,
2. create a user in MariaDB,
3. assign them a database,
4. create tables and fill the database with our data
```bash
$ sudo pacman -Syu mariadb  # use your system's package manager
$ sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
$ cd '/usr' ; /usr/bin/mysqld_safe --datadir='/var/lib/mysql'   # might not be necessary
$ sudo systemctl enable mariadb.service
$ sudo systemctl start mariadb.service
$ sudo mysql_secure_installation   # select 'y' for all options
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
$ su josh # switch back from root your user account
$ cd ~ && git clone https://github.com/joshnatis/fms/
$ mysql -u josh -p
```
```sql
mariadb> USE food_db;
mariadb> SOURCE /home/josh/food_db/sql/load.sql
mariadb> SOURCE /home/josh/food_db/sql/useful_queries.sql
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

[Link to Presentation](https://docs.google.com/presentation/d/1R0Ix9HWxDaEe2nscDfknGjl-VRzGP-tC_3WmjU6wotY/edit?usp=sharing)
