from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('hello/',views.HelloView.as_view()),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('signup/', views.SignUp.as_view(), name='signup' ),
    path('message/',views.MessageView.as_view(),name='messages')
]