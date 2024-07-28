from rest_framework import serializers
from .models import Expense, ExpenseParticipant

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = ['participant', 'contribution']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'title', 'description', 'admin', 'type', 'cost', 'created_at']
