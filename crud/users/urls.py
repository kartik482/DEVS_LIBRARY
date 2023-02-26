from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("login/",views.loginpage,name="login"),
    path("logout/",views.logoutuser,name="logout"),
    path("register/",views.registeruser,name="register"),




    path("",views.profiles,name="profiles"),
    path("profile/<str:pk>",views.userprofiles,name="userprofile"),
    path("account/",views.useraccount,name="account"),
    path("inbox/",views.inbox,name="inbox"),
    path("message/<str:pk>",views.viewmessage,name="viewmessage"),
    path("message/<str:pk>",views.viewmessage,name="viewmessage"),
    path("create-message/<str:pk>",views.createmessage,name="createmessage"),

    path("edit-account/",views.editaccount,name="editaccount"),
    path("add-skill/",views.addskill,name="addskill"),
    path("update-skill/<str:pk>",views.updateskill,name="updateskill"),
    path("delete-skill/<str:pk>",views.deleteskill,name="deleteskill"),
]
