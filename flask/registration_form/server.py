from flask import Flask, render_template, redirect, session, request

app = Flask(__name__)
app.secret_key = 'al;kjdsafklhjkasdljkashjkew'

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/process', methods=["POST"])
def process():
  session['name'] = request.form['name']
  session['favorite_language'] = request.form['favorite_language']
  session['comment'] = request.form['comment']
  return redirect('/success')

@app.route('/success')
def success():
  if not 'name' in session:
    return redirect('/')
  print(session['name'])
  return render_template('success.html')

if __name__ == "__main__":
  app.run(debug=True)