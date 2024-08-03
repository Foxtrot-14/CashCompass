from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from django.http import HttpResponse
from .models import Expense, ExpenseParticipant
from .utils import handle_expense_participants,validate_json_data
from django.shortcuts import get_object_or_404
from .models import Expense, ExpenseParticipant
from .serializers import ExpenseSerializer, ExpenseParticipantSerializer
import pandas as pd
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_list(request):
    try:
        expenses = Expense.objects.filter(
            Q(admin=request.user) | Q(participants__participant=request.user)
        ).distinct()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response({"expenses":serializer.data},status=status.HTTP_200_OK)
    except Expense.DoesNotExist:
        return Response({"error":"no expenses"},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def expense_detail(request, pk):
    try:
        expense = Expense.objects.get(id=pk)
    except Expense.DoesNotExist:
        return Response({"error":"Expense Does Not Exist"},status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'GET':
        participants = ExpenseParticipant.objects.filter(expense=expense)
        expense_serializer = ExpenseSerializer(expense)
        participant_serializer = ExpenseParticipantSerializer(participants, many=True)
        return Response({
            "expense": expense_serializer.data,
            "participants": participant_serializer.data
        },status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ExpenseSerializer(expense, data=request.data,partial=True)
        if serializer.is_valid():
            updated_expense = serializer.save()
            participants_data = request.data.get('participants', [])
            handle_expense_participants(updated_expense, request, participants_data)
            return Response({"expense":serializer.data}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@validate_json_data
def expense_create(request):
    data=request.data
    serializer = ExpenseSerializer(data={
            'title':data['title'],
            'description':data['description'],
            'admin':request.user.id,
            'type':data['type'],
            'cost':data['cost']
        })
    if serializer.is_valid():
        expense = serializer.save()
        participants_data = request.data.get('participants', [])
        handle_expense_participants(expense, request, participants_data)
        return Response({"expense":serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_balance(request, pk):
    if request.method == 'GET':
        try:
            expense = get_object_or_404(Expense, pk=pk)
            participants = ExpenseParticipant.objects.filter(expense=expense)
            participant_balances = {}
            
            for participant in participants:
                participant_balance = participant.contribution
                participant_balances[participant.participant] = participant_balance
            
            df = pd.DataFrame(list(participant_balances.items()), columns=['User', 'Balance'])
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={expense.title}.csv'
            
            df.to_csv(path_or_buf=response, index=False)
            
            return response
        except Exception as e:
            # Log or print the exception for debugging
            print(f"Exception occurred: {e}")
            return HttpResponse("An error occurred while generating the CSV file.", status=500)
    return HttpResponse("Method Not Allowed", status=405)