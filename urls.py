from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.index, name='index'),
    url(r'^signup/', views.SignUp.as_view(), name='signup'),
    url(r'^view_climber/(?P<pk>[0-9]+)/$', views.view_climber, name='view_climber'),
]
