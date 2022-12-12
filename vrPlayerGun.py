from flask import Flask, request, render_template
from flask_mysqldb import MySQL

import flask
import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = '192.168.33.30'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/users', methods=['GET'])
def user_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT idUser, Date_format(create_at,'%d-%m-%Y') AS create_at, status FROM user")
    data = cursor.fetchall()
    resp = flask.Response(json.dumps(data))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/users', methods=['POST'])
def user_post_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("INSERT INTO user (nameUser, create_at, status) VALUES ('%s', current_timestamp(), 1)" % 
                   (data['name_user']))
    mysql.connection.commit()
    cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor2.execute("SELECT LAST_INSERT_ID() as idUser")
    data2 = cursor2.fetchall()
    resp = flask.Response(json.dumps(data2))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/usersAllDetails', methods=['GET'])
def userAllDetails_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT u.idUser, u.nameUser, Date_format(u.create_at,'%d-%m-%Y') AS create_at, u.status, s.score FROM user u INNER JOIN score s ON s.user_iduser = u.idUser")
    data = cursor.fetchall()
    resp = flask.Response(json.dumps(data))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/score', methods=['GET'])
def score_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM score")
    data = cursor.fetchall()
    resp = flask.Response(json.dumps(data))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/score', methods=['POST'])
def score_post_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("INSERT INTO score (user_iduser, score) VALUES ('%i', '%d')" % 
                   (data['user_iduser'], data['score']))
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
