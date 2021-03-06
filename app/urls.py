from app import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^signup_submit/', views.signup_submit, name='signup_submit'),
    url(r'^login/', views.medms_login, name='login'),
    url(r'^login_submit/', views.login_submit, name='login_submit'),
    url(r'^account/', views.account, name='account'),
    url(r'^open_requests/', views.open_requests, name='open_requests'),
    url(r'^open_requests_respond/', views.open_requests_respond, name='open_requests_respond'),
    url(r'^message/newsms/', views.receive_sms, name='smsResponder')
]

