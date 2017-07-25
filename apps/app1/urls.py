from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login), 
    url(r'^register$', views.register), 
    url(r'^process-registration$', views.process_registration), 
    url(r'^process-login$', views.process_login),
    url(r'^logout$', views.logout), 

    
    url(r'^books$', views.books),
    url(r'^books/(?P<book_id>\d+)$', views.book_show),
    url(r'^books/add$', views.add),    
    
    url(r'^create-book$', views.create_book),
    url(r'^users/(?P<user_id>\d+)$', views.user_show),
]
