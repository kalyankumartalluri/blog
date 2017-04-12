from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.test_list, name='test_list'),
    url(r'^test/(?P<pk>\d+)/$', views.test_detail, name='test_detail'),
    url(r'^test/new/$', views.test_new, name='test_new'),
    url(r'^testimport', views.test_testimport, name='test_testimport'),
    url(r'^test/(?P<pk>\d+)/edit/$', views.test_edit, name='test_edit'),
]