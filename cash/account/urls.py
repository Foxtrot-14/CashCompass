from django.urls import path
from .views import registration,login,user_detail,user_friends,autocomplete
urlpatterns = [
    path('register/',registration,name='user_registration'),
    path('login/',login,name='user_login'),
    path('user/',user_detail,name="user_detail"),
    path('user/<int:pk>/',user_detail,name="user_detail"),
    path('search-user/',autocomplete,name="seach_user"),
    path('friends/',user_friends,name="user_friends")
]
