from account.models import User
from .models import ExpenseParticipant

import json
from functools import wraps
from django.http import JsonResponse
from django.core.exceptions import ValidationError

def validate_json_data(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Ensure the request body is JSON
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Content type must be application/json'}, status=400)

        try:
            # Parse the JSON data
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Validate "title"
        if not isinstance(data.get('title'), str):
            return JsonResponse({'error': '"title" must be a string'}, status=400)

        # Validate "description"
        if not isinstance(data.get('description'), str):
            return JsonResponse({'error': '"description" must be a string'}, status=400)

        # Validate "type"
        if not isinstance(data.get('type'), int):
            return JsonResponse({'error': '"type" must be an integer'}, status=400)

        # Validate "participants"
        participants = data.get('participants')
        if not isinstance(participants, list):
            return JsonResponse({'error': '"participants" must be a list'}, status=400)

        for participant in participants:
            if not isinstance(participant, dict):
                return JsonResponse({'error': 'Each participant must be an object'}, status=400)
            if not isinstance(participant.get('participant'), int):
                return JsonResponse({'error': '"participant" in each participant object must be an integer'}, status=400)
            if 'contribution' in participant and not isinstance(participant.get('contribution'), int):
                return JsonResponse({'error': '"contribution" must be an integer if present'}, status=400)

        # Call the actual view
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def get_users_from_participants(request):
        participants_data = request.data.get('participants', [])
        # Extract participant IDs from the participant data
        participant_ids = [int(p['participant']) for p in participants_data]
        users = User.objects.filter(id__in=participant_ids)
        # Create a dictionary to quickly look up users by their ID
        user_dict = {user.id: user for user in users}
        return user_dict,participants_data

def handle_expense_participants(expense, request, participants_data):
    user_dict,participants_data = get_users_from_participants(request=request)
    total = 0
    for participant_data in participants_data:
        user_id = int(participant_data['participant'])
        user = user_dict.get(user_id)
        if user:  # Ensure the user exists
            if expense.type == 1:
                ExpenseParticipant.objects.create(
                    expense=expense,
                    participant=user
                )
            elif expense.type == 2:
                ExpenseParticipant.objects.create(
                    expense=expense,
                    participant=user,
                    contribution=participant_data['contribution']
                )
                total += int(participant_data['contribution'])
            elif expense.type == 3:
                ExpenseParticipant.objects.create(
                    expense=expense,
                    participant=user,
                    contribution=participant_data['contribution']
                )
                total += int(participant_data['contribution'])
    
    if expense.type == 1:
        ExpenseParticipant.objects.create(
            expense=expense,
            participant=request.user
        )
        expense.calculate_contributions()
    elif expense.type == 2:
        ExpenseParticipant.objects.create(
            expense=expense,
            participant=request.user,
            contribution=int(expense.cost) - total
        )
    elif expense.type == 3:
        ExpenseParticipant.objects.create(
            expense=expense,
            participant=request.user,
            contribution=100 - total
        )
        expense.calculate_contributions()