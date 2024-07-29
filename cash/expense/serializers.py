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

    def create(self, validated_data):
        # Ensure the `admin` field is set during creation
        if 'admin' not in validated_data:
            raise serializers.ValidationError({"admin": "This field is required for creation."})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure `admin` field cannot be updated
        if 'admin' in validated_data and validated_data['admin'] != instance.admin:
            raise serializers.ValidationError({"admin": "The admin field cannot be updated."})
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
