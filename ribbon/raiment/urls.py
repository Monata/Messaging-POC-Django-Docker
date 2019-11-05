from django.urls import path
from . import views

urlpatterns = [
    path('api/raiment/', views.ClothingListCreate.as_view()),
]