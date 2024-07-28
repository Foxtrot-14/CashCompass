from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError

def validate_json_request(request):
    # Check if the request content type is JSON
    if request.content_type != 'application/json':
        return Response({'error': 'Content type must be application/json'}, status=status.HTTP_400_BAD_REQUEST)

    # Try to parse the JSON request body
    try:
        data = request.data
    except ParseError:
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    
    return data
