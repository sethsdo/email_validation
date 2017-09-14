from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
mysql = MySQLConnector(app, 'email-address')
app.secret_key = 'ThisIsSecret'


emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success')
def email_list():
    email = mysql.query_db("SELECT id, email,  DATE_FORMAT(created_at, ' %b ' ' %D	' ' %Y' ' %h:' '%i' ' %p') AS created_at FROM emails")
    print email
    return render_template('success.html', all_emails=email)
 
@app.route('/success', methods=['GET', 'POST'])
def create():
    if request.form['email'] == '':
        flash("email entry must be filled...")
    elif not emailRegex.match(request.form['email']):
        flash("Invalid email...")
    else:
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
            'email': request.form['email'],
        }
        mysql.query_db(query, data)
        return redirect('/success')
    return redirect("/")

@app.route('/remove_email/<email_id>', methods=['POST'])
def delete(email_id):
    query = "DELETE FROM emails WHERE id = :id"
    data = {'id': email_id}
    mysql.query_db(query, data)
    return redirect('/')

print mysql.query_db("SELECT * FROM emails")
app.run(debug=True)
