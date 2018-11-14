from django.shortcuts import render, redirect

# Create your views here.
def create(req):
  Comment.objects.validate(req.POST, req.session['user_id'])
  return redirect('/')