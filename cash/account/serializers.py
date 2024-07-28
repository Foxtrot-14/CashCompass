from rest_framework import serializers
from .models import User
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','email','name','password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','email','name']

class UserLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    class Meta:
        model = User
        fields = ['phone','email','password']        