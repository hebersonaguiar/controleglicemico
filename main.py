import json, re, csv, os, datetime, sys, ast
from app import app
from db_config import mysql
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, stream_with_context, g, session
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from json import dumps
from io import StringIO
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
from flask_mysqldb import MySQL
import MySQLdb.cursors


@app.route('/', methods=['GET', 'POST'])
def login():
	# Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
		# Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
		# If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('controle'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')

@app.route('/controle')
def controle():
    # Check if user is loggedin
    if 'loggedin' in session:
        try:
            cur = mysql.connection.cursor()
            cur.execute('''SELECT * FROM glucose;''')
            data = cur.fetchall()
        except Exception as e:
            return redirect(url_for('login'))
        finally:
            cur.close()
            return render_template('controle.html', registers=data)

    # User is not loggedin redirect to login page

    return redirect(url_for('login'))

# @app.route('/registros')
# def registros():
# 	if g.username:
# 		try:
# 			cur = mysql.connection.cursor()
# 			cur.execute('''SELECT * FROM data_card;''')
# 			data = cur.fetchall()	

# 		except Exception as e:
# 			return redirect(url_for('index'))
# 		finally:
# 			cur.close()
# 			return render_template('registros.html', registers=data)

# 	return redirect(url_for('index'))

# CONEXÃO COM O AD
# def conn():
#     server_name = 'adserver'
#     user_name   = ''
#     password    = 'passsvc'
#     server      = Server(server_name, get_info=ALL)
#     conn        = Connection(server, user=user_name, password=password)
#     c           = conn.bind()
#     return conn

# REGRAS DE AUTENTICAÇÃO PARA PÁGINA DE LOGIN
# @app.route('/', methods=['GET','POST'])
# def index():

# 	if request.method == 'POST':
# 		session.pop('username', None)

# 		usernameForm = request.form['username'] 
# 		domain_name = ''
# 		domain      = domain_name.split('.')
# 		connect     = conn()

# 		try:
# 			connect.search('dc={},dc={},dc={}'.format(domain[0], domain[1], domain[2]), '(sAMAccountName={})'.format(usernameForm), attributes = [ 'cn', 'department' ], search_scope=SUBTREE )
# 			obj  = connect.entries[0].cn.value
# 			cn = str(obj)
# 			departmentobj  = connect.entries[0].department.value
# 			department = str(departmentobj)

# 			serverAd = 'adserver'
# 			passwordForm = request.form['password']	

# 			if department == 'Hepta':
# 				userConn = ''.format(cn)	
# 				serverAdConn      = Server(serverAd, get_info=ALL)
# 				connAdHepta        = Connection(serverAdConn, user=userConn, password=passwordForm)
# 				cAd = connAdHepta.bind()
# 				if cAd == True:
# 					session['username'] = request.form['username']
# 					return redirect(url_for('registros'))
# 				else:
# 					return redirect(url_for('index'))
# 			elif department == 'GELTI-COTIC':
# 				print("department: " + department)
# 				userConn = ''.format(cn)				
# 				print(cn + " " + userConn)
# 				serverAdConn      = Server(serverAd, get_info=ALL)
# 				connAdEpl        = Connection(serverAdConn, user=userConn, password=passwordForm)
# 				cAd = connAdEpl.bind()
# 				if cAd == True:
# 					session['username'] = request.form['username']
# 					return redirect(url_for('registros'))
# 				else:
# 					return redirect(url_for('index'))				
# 			else:
# 				return redirect(url_for('index'))

# 			return jsonify({'Conn': cAd}), 200

# 		except Exception as error_message:
# 			return redirect(url_for('index'))

# 	return render_template('index.html')


# @app.route('/registros')
# def registros():
# 	if g.username:
# 		try:
# 			cur = mysql.connection.cursor()
# 			cur.execute('''SELECT * FROM data_card;''')
# 			data = cur.fetchall()	

# 		except Exception as e:
# 			return redirect(url_for('index'))
# 		finally:
# 			cur.close()
# 			return render_template('registros.html', registers=data)

# 	return redirect(url_for('index'))


# @app.route('/api/v1/insert', methods=['POST'])
# def insert():
# 	try:
# 		login = str(request.json.get("login", None))
# 		number_card = str(request.json.get("number_card", None))
# 		created_by = str(request.json.get("created_by", None))
# 		action = str(request.json.get("action", None))
# 		now = datetime.datetime.now()
# 		created_at = str(now.strftime("%Y-%m-%d %H:%M"))

# 		# print("Login: " + login + " Number Card: " + number_card + " Created By: " + created_by + " Action: " + action + " Created At: " + created_at)

# 		cur = mysql.connection.cursor()
# 		cur.execute("INSERT INTO data_card (login, number_card, created_by, action, created_at) VALUES (%s, %s, %s, %s, %s)", (login, number_card, created_by, action, created_at))
# 		mysql.connection.commit()		
# 		cur.close()

# 		return jsonify({'login': login}), 200

# 	except Exception as e:
# 		return jsonify(e), 400

@app.route('/download', methods=['POST', 'GET'])
def download():
    def generate():
        data = StringIO()
        w = csv.writer(data, delimiter=';')

        # write header
        w.writerow(('Id', 'Login', 'Número do Cartão', 'Realizado por', 'Ação', 'Atualizado Em'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM data_card;''')
        data_registers = cur.fetchall()

        data_registers_l = list(data_registers)

        # write each data_registers_l item
        for item in data_registers_l:
            w.writerow((
                item[0],
                item[1],
                item[2],
                item[3],                
                item[4],
                item[5].isoformat()  # format datetime as string
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # add a filename
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='registros.csv')

    # stream the response as the data is generated
    return Response(
        stream_with_context(generate()),
        mimetype='text/csv', headers=headers
    )

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


# # REGRA PARA PÁGINA DE LOGOUT
# @app.route("/logout", methods=['GET','POST'])
# def logout():
# 	if 'username' in session:
# 		g.username = None
# 		dropsession()

# 		return redirect(url_for('index'))

# 	return redirect(url_for('index'))

# @app.before_request
# def before_request():
# 	g.username = None
# 	if 'username' in session:
# 		g.username = session['username']

# @app.route('/getsession')
# def getsession():
# 	if 'username' in session:
# 		return session['username']

# 	return 'Not logged in'

# @app.route('/dropsession')
# def dropsession():
# 	session.pop('username', None)
# 	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port='5000')