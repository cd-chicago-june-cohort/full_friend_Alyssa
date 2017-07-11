from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'full_friends')

@app.route('/')
def index():
    query = 'select concat(first_name, " ", last_name) as name, age, date_format(friend_since, "%b%D") as date, date_format(friend_since, "%Y") as year from friends'
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends = friends)

@app.route('/add_friend', methods = ['POST'])
def add_friend():
    query = 'insert into friends (first_name, last_name, age, friend_since) values(:first_name, :last_name, :age, NOW())'
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'age': request.form['age']    
    }
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)