from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer,UserSerializer,FriendsSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .models import User,Friend
from django.db.models import Q
from .utils import validate_json_request
#Generating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
@api_view(['POST']) 
def registration(request):
    #JSON validation for all requests
    data = validate_json_request(request)
    if isinstance(data, Response):  # Check if it's an error response
        return data
    
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
        'password': make_password(data['password1'])
    })
    
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({'success': 'User registered successfully', 'tokens': tokens}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    #JSON validation for all requests
    if request.method=='POST':
        print(request.data)
        data = validate_json_request(request)
        if isinstance(data, Response):  # Check if it's an error response
            return data
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
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)  # Handle unsupported methods

@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def userDetail(request,pk):
    if request.method=='GET':
        id = pk
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        #Serialize the obtained data
        serializer = UserSerializer(user,partial=True)
        return Response({"user":serializer.data},status=status.HTTP_200_OK)
    elif request.method=='PATCH':
        #JSON validation for all requests
        data = validate_json_request(request)
        if isinstance(data, Response):  # Check if it's an error response
            return data
        id = pk
        if pk != request.user.id:
            return Response({'error':'You are not authorized to make changes'},status=status.HTTP_401_UNAUTHORIZED)
        user = request.user  # Get the authenticated user directly
        serializer = UserRegistrationSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)  # Handle unsupported methods

@api_view(['GET'])
def autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        try:
            users = User.objects.filter(name__icontains=query)
        except User.DoesNotExist:
            return Response({"error":"No User by the Name"},status=status.HTTP_404_NOT_FOUND)
        
    serializer = UserSerializer(users, many=True)
    return Response({"users":serializer.data},status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def user_friends(request):
    if request.method=="GET":
        try:
            friends = Friend.objects.filter(Q(friend_1=request.user.id)|Q(friend_2=request.user.id))
            serializer = FriendsSerializer(friends,many=True)
            return Response({"friends":serializer.data},status=status.HTTP_200_OK)
        except Friend.DoesNotExist:
            return Response({"error":"No friends"},status=status.HTTP_404_NOT_FOUND)
    elif request.method=="POST":
        serializer = FriendsSerializer(data={
            'friend_1':request.user.id,
            'friend_2':request.data["friend"]
        })
        if serializer.is_valid():
            return Response({"friends":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    return Response({"error":"Method Not Allowed"},status=status.HTTP_502_BAD_GATEWAY)