from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/raiment/item', views.ItemListCreate.as_view()),
    path('api/raiment/packlist', views.PacklistListCreate.as_view()),
    path('api/raiment/addtopacklist', views.AddToPacklist.as_view(), name='packlist'),
    path('api/raiment/createtopacklist', views.CreateToPacklist.as_view(), name='createtopacklist'),
    path('api/raiment/getpacklist', views.GetPacklistContent.as_view(), name='packlistcontent'),
    path('api/raiment/folder', views.FolderListCreate.as_view()),
    path('api/raiment/folderhas', views.FolderHasListCreate.as_view()),
    path('hello', views.HelloView.as_view(), name='hello'),
    path('api/raiment/getallclothes', views.GetAllItems.as_view(), name='uitems'),
    path('api/raiment/getclotheswithweather', views.GetClothesWeather.as_view(), name='witems'),
    path('api/raiment/addtoinventory', views.AddToInventory.as_view(), name='inventory'),
    path('api/raiment/login', obtain_auth_token, name='api_token_auth'),
    path('api/raiment/signup', views.SignUp.as_view(), name='signup' ),
    path('api/raiment/type', views.TypeCreate.as_view(), name='type'),
    path('api/raiment/detect',views.ObjectDetect.as_view(),name='objectdetection')
]