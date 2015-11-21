from app import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^message/newsms/$', views.receive_sms, name='smsResponder')
]

