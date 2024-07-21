"""
URL configuration for supernova project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from supernovaback.views import main
import supernovaback.views as views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("main/", views.main.as_view(), name="main"),
    path("loadtimetable/", views.timetable.as_view(), name="loadtimetable"),
    path("gettimetable/", views.gettimetable.as_view(), name="gettimetable"),
    path("start_timer/", views.start_timer.as_view(), name="start_timer"),
    path("stop_timer/", views.stop_timer.as_view(), name="stop_timer"),
    path("timer/", views.timer.as_view(), name="get_timer"),
    path("quiz/", views.quiz.as_view(), name="quiz"),
    path("submit/", views.submit.as_view(), name="submit"),
    path("pet_select/", views.pet_select.as_view(), name="pet_select"),

]


