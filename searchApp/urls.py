"""ePavitram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('policy/', views.policy, name='policy'),
    path('console/', views.console, name='console'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback, name='feedback'),
    path('result/', views.result, name='result'),
    path('ePavitram/', views.searchContent, name='search'),
    path('ajax/', views.ajax, name='ajax'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('getcontact/', views.getContact,name='getcontact'),
    path("getfeedback/",views.getFeedback,name='getfeedback'),
    path("getSitemap/",views.getSitemap,name='getsitemap'),
    path("studyhome/",views.studyhome,name='studyhome'),
    path("n_jobs_on_two_machiens.html/",views.n_jobs_on_two_machiens,name='n_jobs_on_two_machiens'),
    path("cal_n_jobs_on_two_machiens/",views.cal_n_jobs_on_two_machiens,name='cal_n_jobs_on_two_machiens'),
    path("pdf/",views.getPdf,name='pdf'),
    path("getsignup/" , views.getsignup , name='getsignup'),
    path("check_login/",views.check_login,name='check_login'),
    path("check_console/",views.check_console,name='check_console'),
    path("log_out/",views.log_out,name='log_out'),
    path("gameTheory/",views.gameTheory,name='gameTheory'),
    path("gametheory/",views.gametheory,name='gametheory'),

]
