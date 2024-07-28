from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .utils import get_users_from_participants
from account.models import User
from .models import Expense, ExpenseParticipant
from .serializers import ExpenseSerializer, ExpenseParticipantSerializer
from account.utils import validate_json_request
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def expense_list(request):
    #JSON validation for all requests
    data = validate_json_request(request)
    if isinstance(data, Response):  # Check if it's an error response
        return data
    if request.method == 'GET':
        expenses = Expense.objects.all(admin=9)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExpenseSerializer(data={
            'title':data['title'],
            'description':data['description'],
            'admin':request.user.id,
            'type':data['type'],
            'cost':data['cost']
        },partial=True)
        if serializer.is_valid():
            expense = serializer.save()
            if expense.type==1:
                user_dict,participants_data = get_users_from_participants(request=request)
                for participant_data in participants_data:
                    user_id = int(participant_data['participant'])
                    user = user_dict.get(user_id)
                    if user:  # Ensure the user exists
                        ExpenseParticipant.objects.create(
                            expense=expense,
                            participant=user
                        )
                ExpenseParticipant.objects.create(
                            expense=expense,
                            participant=request.user
                        )        
                expense.calculate_contributions()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif expense.type==2:
                user_dict,participants_data = get_users_from_participants(request=request)
                total=0
                for participant_data in participants_data:
                    user_id = int(participant_data['participant'])
                    user = user_dict.get(user_id)
                    if user:  # Ensure the user exists
                        ExpenseParticipant.objects.create(
                            expense=expense,
                            participant=user,
                            contribution=participant_data['contribution']
                        )
                        total = total+int(participant_data['contribution'])
                ExpenseParticipant.objects.create(
                            expense=expense,
                            participant=request.user,
                            contribution=int(data['cost'])-total
                        )
            elif expense.type==3:
                user_dict,participants_data = get_users_from_participants(request=request)
                total=0
                for participant_data in participants_data:
                    user_id = int(participant_data['participant'])
                    user = user_dict.get(user_id)
                    if user:  # Ensure the user exists
                        ExpenseParticipant.objects.create(
                            expense=expense,
                            participant=user,
                            contribution=participant_data['contribution']
                        )
                        total = total+int(participant_data['contribution'])
                ExpenseParticipant.objects.create(
                            expense=expense,
                            participant=request.user,
                            contribution=100-total
                        )
                expense.calculate_contributions()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                pass
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
def expense_detail(request, pk):
    #JSON validation for all requests
    data = validate_json_request(request)
    if isinstance(data, Response):  # Check if it's an error response
        return data
    
    try:
        expense = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            expense = serializer.save()
            # Clear existing participants and re-add them
            ExpenseParticipant.objects.filter(expense=expense).delete()
            participants_data = request.data.get('participants', [])
            for participant_data in participants_data:
                ExpenseParticipant.objects.create(
                    expense=expense,
                    participant=participant_data['participant'],
                    contribution=participant_data['contribution']
                )
            expense.calculate_contributions()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def expense_participant_list(request):
    #JSON validation for all requests
    data = validate_json_request(request)
    if isinstance(data, Response):  # Check if it's an error response
        return data
    if request.method == 'GET':
        participants = ExpenseParticipant.objects.all()
        serializer = ExpenseParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExpenseParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
