from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.home,name="home"),
    path('project/<str:pk>', views.projectobj,name="project"),
    path('create-project/', views.createproject,name="create-project"),
    path('update-project/<str:pk>', views.updateproject,name="updateproject"),
    path('delete-project/<str:pk>', views.deleteproject,name="deleteproject"),
]