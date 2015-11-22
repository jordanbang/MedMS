from app import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup_submit/', views.signup_submit, name='signup_submit'),
    url(r'^open_requests/', views.open_requests, name='open_requests'),
    url(r'^message/newsms/$', views.receive_sms, name='smsResponder')
]

