from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
  def validate(self, form):
    errors = []

    if len(form['first_name']) < 3:
      errors.append("First name must be at least 3 characters long")
    if len(form['last_name']) < 3:
      errors.append("Last name must be at least 3 characters long")
    if len(form['username']) < 3:
      errors.append("Username must be at least 3 characters long")
    if not EMAIL_REGEX.match(form['email']):
      errors.append("Email must be valid")
    if len(form['password']) < 8:
      errors.append("Password must be at least 8 characters long")
    
    # check to see if email exists in db
    # try:
    #   self.get(email=form['email'])
    #   errors.append("Email already in use")
    # except:
    #   pass

    user_list = self.filter(email=form['email'])
    if len(user_list) > 0:
      errors.append("Email already in use")

    user_list = self.filter(username=form['username'])
    if len(user_list) > 0:
      errors.append("Username already in use")

    return errors

  def create_user_with_hashed_password(self, form):
    pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
    user = self.create(
      first_name = form['first_name'],
      last_name = form['last_name'],
      email = form['email'],
      username = form['username'],
      pw_hash = pw_hash
    )
    return user

  def login(self, form):
    errors = []

    try:
      user = self.get(email=form['email'])
      if not bcrypt.checkpw(form['password'].encode(), user.pw_hash.encode()):
          errors.append("Email or password incorrect.")
    except:
      errors.append("Email or password incorrect.")

    if len(errors) > 0:
      return (False, errors)
    else:
      return (True, user)
  
  def create_friend_request(self, form, sender_id):
    sent_by = self.get(id = sender_id)
    sent_to = self.get(id = form['request_to'])
    print(sent_by, sent_to)
    Request.objects.create(request_from = sent_by, request_to = sent_to)
  
  def delete_friend_request(self, form, user_id):
    sent_by = self.get(id = user_id)
    sent_to = self.get(id = form['request_to'])
    requests = Request.objects.filter(request_from = sent_by).filter(request_to = sent_to)
    if requests:
      requests[0].delete()

class User(models.Model):
  first_name = models.CharField(max_length = 255)
  last_name = models.CharField(max_length = 255)
  username = models.CharField(max_length = 255)
  email = models.CharField(max_length = 255)
  pw_hash = models.CharField(max_length = 500)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = UserManager()

  def __str__(self):
    return self.username

class Request(models.Model):
  request_from = models.ForeignKey(User, related_name = "requests_sent")
  request_to = models.ForeignKey(User, related_name = "requests_received")