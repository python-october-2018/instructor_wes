from flask import Flask, session, render_template, redirect, flash, request
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = 'alsdkfja;lsjkdskdslafjklds'

@app.route('/')
def index():
  if 'user' not in session:
    session['user'] = None

  db = connectToMySQL("oct_ninja_gold")
  # query = 'SELECT * FROM users'
  # db.query_db(query)
  users_list = db.query_db('SELECT * FROM users')
  # print("*" * 80)
  # print(users_list)
  # print("*" * 80)

  # db = connectToMySQL("oct_ninja_gold")
  # query = 'SELECT * FROM users WHERE email = %(email)s'
  # data = {
  #   "email": "wharper@codingdojo.com"
  # }
  # specific_user_results = db.query_db(query, data)
  # single_user = specific_user_results[0]
  return render_template('index.html', users=users_list)

@app.route('/process', methods=['POST'])
def process():
  print("*" * 80)
  print(request.form)

  db = connectToMySQL("oct_ninja_gold")
  query = 'SELECT * FROM users WHERE email = %(email)s'
  data = {
    'email': request.form['email']
  }
  result_list = db.query_db(query, data)
  if len(result_list) > 0:
    session['user'] = result_list[0]
  else:
    session['user'] = None

  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True)