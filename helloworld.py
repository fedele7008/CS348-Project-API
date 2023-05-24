from flask import Flask, render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'group8'
app.config['MYSQL_PASSWORD'] = 'Password0!'
app.config['MYSQL_DB'] = 'testDB'
 
mysql = MySQL(app)

@app.route('/')
def hello():
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * from FOOD ''')
        result = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return str(result)
