from flask import Flask, session, render_template, redirect, flash, request
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt

import re
import random

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'alsdkfja;lsjkdskdslafjklds'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/dashboard')
def dashboard():
  if 'user_id' not in session:
    return redirect('/')
  
  db = connectToMySQL('oct_ninja_gold')
  query = "SELECT * FROM users WHERE id=%(user_id)s"
  data = {
    'user_id': session['user_id']
  }
  user_list = db.query_db(query, data)
  user = user_list[0]

  db = connectToMySQL('oct_ninja_gold')
  locations_query = "SELECT * FROM locations;"
  locations = db.query_db(locations_query)

  db = connectToMySQL('oct_ninja_gold')
  activities_query = "SELECT activities.gold_amount AS gold_amount, locations.name AS name, activities.created_at AS time FROM activities JOIN locations ON activities.location_id = locations.id WHERE user_id=%(user_id)s ORDER BY activities.created_at DESC;"
  data = {
    'user_id': session['user_id']
  }
  activities_list = db.query_db(activities_query, data)

  return render_template('dashboard.html', email=user['email'], gold=user['gold'], locations=locations, activities=activities_list)

@app.route('/process', methods=['POST'])
def process():
  db = connectToMySQL('oct_ninja_gold')
  location_query = "SELECT * FROM locations WHERE id=%(location_id)s"
  data = {
    "location_id": request.form['location']
  }
  location_list = db.query_db(location_query, data)
  location = location_list[0]

  curr_gold = random.randint(int(location['min_gold']), int(location['max_gold']))

  db = connectToMySQL('oct_ninja_gold')
  activity_insert_query = 'INSERT INTO activities (gold_amount, user_id, location_id, created_at, updated_at) VALUES(%(gold)s, %(user_id)s, %(location_id)s, NOW(), NOW());'
  data = {
    "gold": curr_gold,
    "user_id": session['user_id'],
    "location_id": location['id']
  }
  db.query_db(activity_insert_query, data)

  db = connectToMySQL('oct_ninja_gold')
  user_gold_query = "SELECT gold FROM users WHERE id=%(user_id)s;"
  data = {
    'user_id': session['user_id']
  }
  user_list = db.query_db(user_gold_query, data)
  user = user_list[0]

  db = connectToMySQL('oct_ninja_gold')
  user_update_gold = 'UPDATE users SET gold = %(new_amount)s WHERE id=%(user_id)s;'
  data = {
    'new_amount': int(user['gold']) + curr_gold,
    'user_id': session['user_id']
  }
  db.query_db(user_update_gold, data)
  return redirect('/dashboard')

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

@app.route('/login', methods=['POST'])
def login():
  db = connectToMySQL('oct_ninja_gold')
  query = "SELECT pw_hash, id FROM users WHERE email=%(email)s;"
  data = {
    'email': request.form['email']
  }
  result = db.query_db(query, data)

  if len(result) == 0:
    flash("Email or password incorrect")
    return redirect('/')
  
  user = result[0]
  print("*" * 80)
  print(user)
  print(request.form['password'])
  if not bcrypt.check_password_hash(user['pw_hash'], request.form['password']):
    flash("Email or password incorrect")
    return redirect('/')

  session['user_id'] = user['id']
  return redirect('/dashboard')

@app.route('/new_location')
def new_location():
  return render_template('new_location.html')

@app.route('/create_location', methods=['POST'])
def create_location():
  errors = False

  if len(request.form['name']) < 3:
    flash("Name must be at least 3 characters")
    errors = True

  try:
    max_gold = int(request.form['max_gold'])
    min_gold = int(request.form['min_gold'])

    if min_gold > max_gold:
      flash("Max Gold must be greater than Min Gold")
      errors = True
  except:
    flash("Max/Min gold must be integers")
    errors = True

  if errors == True:
    return redirect('/new_location')
  else:
    # create location
    db = connectToMySQL('oct_ninja_gold')
    insert_query = 'INSERT INTO locations (name, max_gold, min_gold, created_at, updated_at) VALUES (%(name)s, %(max_gold)s, %(min_gold)s, NOW(), NOW());'
    data = {
      "name": request.form['name'].lower(),
      "max_gold": max_gold,
      "min_gold": min_gold
    }
    db.query_db(insert_query, data)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True)