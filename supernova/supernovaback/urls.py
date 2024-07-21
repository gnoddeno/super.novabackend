# example 앱에 대한 url 설정
from django.urls import path, include
import supernovaback.views as views

urlpatterns = [
    path("main/", views.main.as_view(), name="main"),
    ]
