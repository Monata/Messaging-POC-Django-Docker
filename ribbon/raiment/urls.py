from django.urls import path
from . import views

urlpatterns = [
    path('api/raiment/item', views.ItemListCreate.as_view()),
    path('api/raiment/packlist', views.PacklistListCreate.as_view()),
    path('api/raiment/folder', views.FolderListCreate.as_view()),
    path('api/raiment/folderhas', views.FolderHasListCreate.as_view()),

    path('api/Login/<int:username>/<slug:userpass>', views.Login.as_view()),
    path('api/clothingGroup/', views.ClothingGroup.as_view()),
    path('api/clothingItem/', views.ClothingItem.as_view())
]