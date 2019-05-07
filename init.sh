
#!/usr/bin/env bash

# Refresh Bash Profile For Environment Variables
source ~/.bash_profile

# Setting Up For DEV_DATABASE_URL LINK
if [ -z "$DEV_DATABASE_URL" ];then
    echo 'Please Enter Your Mysql Connection URL (example: mysql+pymysql://root:password@localhost:3306/inspection)': 
    read mysql_connection_url_input
    export 'DEV_DATABASE_URL=$mysql_connection_url_input'
else
    echo "Please Verify Your Mysql Connection URL: $DEV_DATABASE_URL (y/n)?"
    read mysql_connection_url_confirm
    if [ "$mysql_connection_url_confirm" == "${mysql_connection_url_confirm#[Yy]}" ] ;then
        echo 'Please Enter Your Mysql Connection URL (example: mysql+pymysql://root:password@localhost:3306/inspection)': 
        read mysql_connection_url_input
        export 'DEV_DATABASE_URL=$mysql_connection_url_input'
    fi
fi

# Preparing For Migration
source ../myvenv/bin/activate
rm -fr migrations

# Drop The Old Exsist Database
echo "Please enter your Mysql root password !"
read -s MYSQL_PWD
mysql -u root -p$MYSQL_PWD -Bse 'DROP DATABASE IF EXISTS Inspection; CREATE DATABASE Inspection CHARACTER SET utf8'
echo 'Finished Refreshed Database'

# Python Mysql Migration
python manage.py db init
python manage.py db migrate -m "initial migration"
python manage.py db upgrade
echo 'Finished Migration'

# SQL Seed Data Injection
mysql -u root -p$MYSQL_PWD < seed.sql
