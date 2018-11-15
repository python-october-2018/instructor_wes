from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Comment

# Create your views here.
def create(req):
  errors = Comment.objects.validate(req.POST)
  if len(errors) > 0:
    # flash messages
    for error in errors:
      messages.error(req, error)
  else:
    Comment.objects.create_comment(req.POST, req.session['user_id'])
  return redirect('/')