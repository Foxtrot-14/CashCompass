from django.urls import path
from .views import expense_list, expense_detail, expense_participant_list

urlpatterns = [
    path('expense/', expense_list, name='expense-list'),
    path('expense/<int:pk>/', expense_detail, name='expense-detail'),
    path('expense-participants/', expense_participant_list, name='expense-participant-list'),
]
