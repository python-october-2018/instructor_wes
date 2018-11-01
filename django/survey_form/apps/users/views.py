from django.shortcuts import render, redirect

# Create your views here.
def index(request):
  context = {
    "color": "red",
    "number": 42
  }
  return render(request, 'users/index.html', context)

def process(req):
  if req.method != "POST":
    return redirect('/')

  req.session['name'] = req.POST['name']
  req.session['favorite_language'] = req.POST['favorite_language']
  return redirect("/success")

def success(request):
  return render(request, 'users/success.html')

def colors(req, color):
  print(color)
  context = {
    "col": color
  }
  return render(req, 'users/colors.html', context)