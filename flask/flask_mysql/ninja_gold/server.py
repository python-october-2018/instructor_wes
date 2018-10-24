from flask import Flask, session, render_template, redirect, flash, request
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt

import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'alsdkfja;lsjkdskdslafjklds'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/users/create', methods=["POST"])
def users_create():
  error = False

  if not EMAIL_REGEX.match(request.form['email']):
    flash("Email must be valid")
    error = True

  if len(request.form['password']) < 8:
    flash('Password must be at least 8 characters long.')
    error = True

  if request.form['password'] != request.form['confirm']:
    flash('Password and confirm password must match.')
    error = True

  if error == True:
    return redirect('/')
  else:
    # check if user exists with entered email
    db = connectToMySQL('oct_ninja_gold')
    unique_query = 'SELECT id FROM users WHERE email = %(email)s;'
    unique_data = {
      'email': request.form['email']
    }
    user_list = db.query_db(unique_query, unique_data)
    if len(user_list) > 0:
      flash('Email already in use')
      return redirect('/')

    # hash password
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])

    # create user
    db = connectToMySQL('oct_ninja_gold')
    query = 'INSERT INTO users (email, pw_hash, gold, created_at, updated_at) VALUES(%(email)s, %(pw_hash)s, 0, NOW(), NOW());'
    data = {
      'email': request.form['email'],
      'pw_hash': hashed_pw
    }
    db.query_db(query, data)
    return redirect('/')

if __name__ == "__main__":
  app.run(debug=True)