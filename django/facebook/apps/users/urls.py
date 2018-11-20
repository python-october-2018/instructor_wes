from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^new/$', views.new, name="new"),
  url(r'^create/$', views.create, name="create"),
  url(r'^login/$', views.login, name="login"),
  url(r'^logout/$', views.logout, name="logout"),
  url(r'^create_request/$', views.create_request, name="create_request"),
  url(r'^remove_request/$', views.remove_request, name="remove_request"),
]
