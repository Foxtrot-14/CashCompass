from django.urls import path
from .views import registration,login,userDetail
urlpatterns = [
    path('register/',registration,name='user_registration'),
    path('login/',login,name='user_login'),
    path('user/<int:pk>/',userDetail,name="user_detail")
]
