from django.urls import path
from . import views

urlpatterns = [
    path('hello/',views.HelloView.as_view()),
    path('login/', views.Login.as_view(), name='api_token_auth'),
    path('signup/', views.SignUp.as_view(), name='signup' ),
    path('message/',views.MessageView.as_view(),name='messages'),
    path('block/',views.BlockView.as_view(),name='block'),
]