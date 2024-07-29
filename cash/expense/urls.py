from django.urls import path
from .views import expense_list, expense_detail, expense_balance,expense_create

urlpatterns = [
    path('expense/', expense_list, name='expense-list'),
    path('expense/<int:pk>/', expense_detail, name='expense-detail'),
    path('expense-create/', expense_create, name='expense-create'),
    path('balance-sheet/<int:pk>/', expense_balance, name='expense-balancesheet'),
]
