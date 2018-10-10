from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
  my_list = ['Wes', 'Adam', 'Luke', 'Sinsath', 'Jalen', 'Bernard', 'Paul']
  return render_template('index.html', names=my_list)

@app.route('/colors/<color>')
def other(color):
  return render_template('other.html', col=color)

@app.route('/form')
def form():
  return render_template('form.html')

@app.route('/process', methods=['POST'])
def process():
  print('*' * 80)
  print(request.form)
  print('*' * 80)
  return redirect('/form')

if __name__ == "__main__":
  app.run(debug=True)