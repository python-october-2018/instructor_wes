from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(req):
  if 'user_id' not in req.session:
    return redirect('/users/new')

  return render(req, 'users/index.html')

def new(req):
  return render(req, 'users/new.html')

def create(req):
  errors = User.objects.validate(req.POST)
  if len(errors) > 0:
    # flash all error messages
    for error in errors:
      messages.error(req, error)
  else:
    # hash password and create user
    user = User.objects.create_user_with_hashed_password(req.POST)
    req.session['user_id'] = user.id
    return redirect('/')
  return redirect('/users/new')

def login(req):
  valid, result = User.objects.login(req.POST)
  if valid == False:
    for error in result:
      messages.error(req, error)
  else:
    req.session['user_id'] = result.id
    return redirect('/')
  return redirect('/users/new')