from django.db import models
from django.utils.translation import gettext_lazy as _

class Expense(models.Model):
    EXPENSE_TYPE = (
        (1, _("Equal")),
        (2, _("Exact")),
        (3, _("Percentage")),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"), help_text=_("Provide a detailed description of the expense."))
    admin = models.ForeignKey(
        "account.User",
        verbose_name=_("Admin User"),
        on_delete=models.CASCADE,
        related_name='expenses_administered',
    )
    type = models.PositiveSmallIntegerField(choices=EXPENSE_TYPE, verbose_name=_("Expense Type"))
    cost = models.IntegerField(blank=False, verbose_name=_("Total cost of expense"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    def calculate_contributions(self):
        if self.type == 1:
            # Equal split
            participants = self.participants.all()
            num_participants = participants.count()
            if num_participants == 0:
                return
            contribution_amount = self.cost / num_participants

            for participant in participants:
                participant.contribution = contribution_amount
                participant.save()
    
        elif self.type == 2:
        # Exact split
            participants = self.participants.all()
        # Validate contributions
            total_contributed = sum(p.contribution for p in participants)
            if total_contributed != self.cost:
                raise ValueError("The total contributions do not match the total cost of the expense.")

        elif self.type == 3:
            # Percentage split
            participants = self.participants.all()
            total_percentage = sum(p.contribution for p in participants)  # Assuming contribution holds percentage

            if total_percentage != 100:
                raise ValueError("The total percentage contributions must add up to 100.")

            for participant in participants:
                percentage = participant.contribution
                contribution_amount = (percentage / 100) * self.cost
                participant.contribution = contribution_amount
                participant.save()
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")
        ordering = ['-created_at', 'title']


class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(
        Expense,
        on_delete=models.CASCADE,
        related_name='participants',
    )
    participant = models.ForeignKey(
        "account.User",
        verbose_name=_("ParticipantUser"),
        on_delete=models.CASCADE,
        related_name='participant_expense',
    )
    contribution = models.FloatField(verbose_name=_("Contribution of Participant"),default=0)
    
    class Meta:
        unique_together = ('expense', 'participant')

    def __str__(self):
        return f"{self.participant} - {self.expense}"