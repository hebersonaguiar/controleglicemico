#!/bin/bash

set -e

help() {
    echo "Usage: docker run -dti --link mysql:mysql -e MYSQL_HOST=value5 -e MYSQL_USER=value6 -e MYSQL_PASS=value7 -e MYSQL_DB=value8 -e MYSQL_PORT=value9 image:tag" >&2
    echo
    echo "   MYSQL_HOST          hostname mysql database"
    echo "   MYSQL_USER          user for connecting the mysql database"
    echo "   MYSQL_PASS          passowrd of user for connecting the database"
    echo "   MYSQL_DB            name database for connect "
    echo "   MYSQL_PORT          port database for connect "
    echo
    exit 1
}

if [ ! -z "$MYSQL_HOST" ] || [ ! -z "$MYSQL_USER" ] || [ ! -z "$MYSQL_PASS" ] || [ ! -z "$MYSQL_DB" ] || [ ! -z "$MYSQL_PORT" ]; then

	sed -i "s/mysqlhost/$MYSQL_HOST/g" /opt/db_config.py
	sed -i "s/mysqluser/$MYSQL_USER/g" /opt/db_config.py
	sed -i "s/mysqlpass/$MYSQL_PASS/g" /opt/db_config.py
	sed -i "s/dbmysql/$MYSQL_DB/g" /opt/db_config.py
    sed -i "s/mysqlport/$MYSQL_PORT/g" /opt/db_config.py

else
	echo "Please enter the required data!"
	help

fi

exec "$@"