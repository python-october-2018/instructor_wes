from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post

# Create your views here.
def index(req):
  if 'user_id' not in req.session:
    return redirect('/users/new')

  context = {
    'posts': Post.objects.all()
  }
  return render(req, 'posts/index.html', context)

def create(req):
  errors = Post.objects.validate(req.POST)
  if len(errors) > 0:
    # flash error messages
    for error in errors:
      messages.error(req, error)
  else:
    # create message
    Post.objects.create_post(req.POST, req.session['user_id'])
  return redirect('/')