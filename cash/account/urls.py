from django.urls import path
from .views import registration,login,userDetail,user_friends,autocomplete
urlpatterns = [
    path('register/',registration,name='user_registration'),
    path('login/',login,name='user_login'),
    path('user/<int:pk>/',userDetail,name="user_detail"),
    path('search-user/',autocomplete,name="seach_user"),
    path('friends/',user_friends,name="user_friends")
]
