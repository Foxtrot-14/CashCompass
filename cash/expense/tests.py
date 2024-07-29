from django.test import TestCase
from account.models import User
from .models import Expense, ExpenseParticipant

class ExpenseModelTests(TestCase):

    def setUp(self):
        # Create users with name, email, and phone
        self.user1 = User.objects.create_user(
            name='User One',
            email='user1@example.com',
            phone='1234567890',
            password='pass'
        )
        self.user2 = User.objects.create_user(
            name='User Two',
            email='user2@example.com',
            phone='0987654321',
            password='pass'
        )

    def test_equal_split(self):
        from expense.models import Expense, ExpenseParticipant  # Import locally to avoid circular import issues

        # Create an expense
        expense = Expense.objects.create(
            title="Dinner",
            description="Dinner with friends",
            admin=self.user1,
            type=1,  # Equal split
            cost=100
        )

        # Add participants
        ExpenseParticipant.objects.create(expense=expense, participant=self.user1)
        ExpenseParticipant.objects.create(expense=expense, participant=self.user2)

        # Call calculate_contributions
        expense.calculate_contributions()

        # Check contributions
        participants = ExpenseParticipant.objects.filter(expense=expense)
        self.assertEqual(participants.count(), 2)
        for participant in participants:
            self.assertEqual(participant.contribution, 50)

    def test_exact_split(self):
        from expense.models import Expense, ExpenseParticipant  # Import locally to avoid circular import issues

        # Create an expense
        expense = Expense.objects.create(
            title="Lunch",
            description="Lunch with colleagues",
            admin=self.user1,
            type=2,  # Exact split
            cost=80
        )

        # Add participants with exact contributions
        ExpenseParticipant.objects.create(expense=expense, participant=self.user1, contribution=50)
        ExpenseParticipant.objects.create(expense=expense, participant=self.user2, contribution=30)

        # Call calculate_contributions and expect no errors
        try:
            expense.calculate_contributions()
        except ValueError:
            self.fail("calculate_contributions raised ValueError unexpectedly!")

    def test_percentage_split(self):
        from expense.models import Expense, ExpenseParticipant  # Import locally to avoid circular import issues

        # Create an expense
        expense = Expense.objects.create(
            title="Movie",
            description="Movie night",
            admin=self.user1,
            type=3,  # Percentage split
            cost=120
        )

        # Add participants with percentage contributions
        ExpenseParticipant.objects.create(expense=expense, participant=self.user1, contribution=50)
        ExpenseParticipant.objects.create(expense=expense, participant=self.user2, contribution=50)

        # Call calculate_contributions
        expense.calculate_contributions()

        # Check contributions
        participants = ExpenseParticipant.objects.filter(expense=expense)
        self.assertEqual(participants.count(), 2)
        for participant in participants:
            self.assertEqual(participant.contribution, 60)

    def test_percentage_split_invalid_total(self):
        from expense.models import Expense, ExpenseParticipant  # Import locally to avoid circular import issues

        # Create an expense
        expense = Expense.objects.create(
            title="Concert",
            description="Concert tickets",
            admin=self.user1,
            type=3,  # Percentage split
            cost=200
        )

        # Add participants with incorrect total percentage
        ExpenseParticipant.objects.create(expense=expense, participant=self.user1, contribution=70)
        ExpenseParticipant.objects.create(expense=expense, participant=self.user2, contribution=40)

        # Call calculate_contributions and expect an error
        with self.assertRaises(ValueError):
            expense.calculate_contributions()

    def test_expense_participant_uniqueness(self):
        from expense.models import Expense, ExpenseParticipant  # Import locally to avoid circular import issues

        # Create an expense
        expense = Expense.objects.create(
            title="Trip",
            description="Weekend trip",
            admin=self.user1,
            type=1,  # Equal split
            cost=200
        )

        # Add a participant
        ExpenseParticipant.objects.create(expense=expense, participant=self.user2, contribution=100)

        # Attempt to create a duplicate participant for the same expense
        with self.assertRaises(Exception) as context:
            ExpenseParticipant.objects.create(expense=expense, participant=self.user2, contribution=100)

        self.assertTrue('UNIQUE constraint failed' in str(context.exception))
