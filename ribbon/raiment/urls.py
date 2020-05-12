from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/raiment/item', views.ItemListCreate.as_view()),
    path('api/raiment/packlist', views.PacklistListCreate.as_view()),
    path('api/raiment/folder', views.FolderListCreate.as_view()),
    path('api/raiment/folderhas', views.FolderHasListCreate.as_view()),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]