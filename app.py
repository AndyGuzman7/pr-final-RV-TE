from flask import Flask, request, render_template
from flask_mysqldb import MySQL

import flask
import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dbcontainer'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
#app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/students', methods=['GET'])
def student_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM student')
    data = cursor.fetchall()
    resp = flask.Response(json.dumps(data))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/students', methods=['POST'])
def student_post_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("INSERT INTO student (first_name, last_name, city, semester) VALUES ('%s', '%s', '%s', %i)" % 
                   (data['first_name'], data['last_name'], data['city'], data['semester']))
    
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/students', methods=['PUT'])
def student_put_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("UPDATE student SET first_name='%s', last_name='%s', city='%s', semester=%i WHERE id=%i" % 
                   (data['first_name'], data['last_name'], data['city'], data['semester'], data['id']))
    
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/studentlist', methods=['GET'])
def student_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM student')
    data = cursor.fetchall()
    return render_template('list.html', students=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
