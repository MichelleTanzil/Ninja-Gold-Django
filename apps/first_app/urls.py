from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^reset$', views.reset),
    url(r'^process_money/(?P<location>\w+)$', views.process_money),
    url(r'^start$', views.win_conditions),
]