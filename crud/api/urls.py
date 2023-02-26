from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('',views.getroutes),
    
    
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('projects/',views.getprojects),
    path('projects/<str:pk>',views.getproject),#get single project
    path('projects/<str:pk>/vote',views.projectvote),#get single project
]
