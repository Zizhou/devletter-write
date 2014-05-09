from django.conf.urls import patterns, url

from write import views

urlpatterns = patterns('',
    url(r'(?P<letter_id>\d+)/$', views.letter, name = 'letter'),
    url(r'^$', views.example, name = 'example'),

)
