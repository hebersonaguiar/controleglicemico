from app import app
from flask_mysqldb import MySQL
import MySQLdb.cursors

# DADOS DE CONEXÃO NA BASE DE CONHECIMENTO
app.config['MYSQL_HOST'] = 'mysqlhost'
app.config['MYSQL_PORT'] = mysqlport
app.config['MYSQL_USER'] = 'mysqluser'
app.config['MYSQL_PASSWORD'] = 'mysqlpass'
# app.config['MYSQL_PASSWORD'] = '71UjqFIgyzEG'
app.config['MYSQL_DB'] = 'dbmysql'
# app.config['MYSQL_DB'] = 'registercardcontrol'

mysql = MySQL(app)