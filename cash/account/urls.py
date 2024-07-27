from django.urls import path
from .views import registration,login
urlpatterns = [
    path('register/',registration,name='user_registration'),
    path('login/',login,name='user_login')
]
