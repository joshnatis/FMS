# food_db
Food Management System (CS 435)

## Setup
These are directions to:
1. install MariaDB (a free and open source version of MySQL) on Arch Linux,
2. create a user in mariadb,
3. assign them a database,
4. create tables and fill the database with our data
5. set up MySQL connector for Python
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
```bash
$ pip install mysql-connector-python
```
