from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.exceptions import ParseError
from .serializers import UserRegistrationSerializer
from rest_framework import status
from .models import User
from django.db.models import Q
#Generating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
@api_view(['POST'])
# @permission_classes([IsAuthenticated])   
def registration(request):
    # Check if the request content type is JSON
    if request.content_type != 'application/json':
        return Response({'error': 'Content type must be application/json'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Try to parse the JSON request body
    try:
        data = request.data
    except ParseError:
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check for required fields
    required_fields = ['phone', 'email', 'name', 'password1', 'password2']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return Response({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    if data['password1'] != data['password2']:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserRegistrationSerializer(data={
        'phone': data['phone'],
        'email': data['email'],
        'name': data['name'],
        'password': data['password1']
    })
    
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({'success': 'User registered successfully', 'tokens': tokens}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    # Check if the request content type is JSON
    if request.content_type != 'application/json':
        return Response({'error': 'Content type must be application/json'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Try to parse the JSON request body
    try:
        data = request.data
    except ParseError:
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check for required fields
    required_fields = ['identifier', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return Response({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    identifier = data['identifier']
    password = data['password']
    
    # Try to find user by email or phone
    try:
        user = User.objects.get(Q(email=identifier) | Q(phone=identifier))
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check password
    if not user.check_password(password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Generate tokens
    tokens = get_tokens_for_user(user)
    
    return Response({'success': 'User logged in successfully', 'tokens': tokens}, status=status.HTTP_200_OK)
   