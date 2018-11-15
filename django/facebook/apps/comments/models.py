from django.db import models
from ..posts.models import Post
from ..users.models import User

# Create your models here.
class CommentManager(models.Manager):
  def validate(self, form):
    errors = []

    if len(form['content']) < 1:
      errors.append('Must have some content')

    return errors

  def create_comment(self, form, user_id):
    try:
      user = User.objects.get(id=user_id)
      post = Post.objects.get(id=form['post_id'])
      self.create(
        content = form['content'],
        creator = user,
        post = post
      )
    except:
      print('SOMETHING WENT WRONG CREATING COMMENT')

class Comment(models.Model):
  content = models.TextField()
  creator = models.ForeignKey(User, related_name="comments")
  post = models.ForeignKey(Post, related_name="comments")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = CommentManager()

  def full_name():
    full_name = self.first_name + self.last_name
    return full_name