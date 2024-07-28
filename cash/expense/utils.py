from account.models import User

def get_users_from_participants(request):
        participants_data = request.data.get('participants', [])
        # Extract participant IDs from the participant data
        participant_ids = [int(p['participant']) for p in participants_data]
        users = User.objects.filter(id__in=participant_ids)
        # Create a dictionary to quickly look up users by their ID
        user_dict = {user.id: user for user in users}
        return user_dict,participants_data