from django.contrib import admin
from .models import Expense, ExpenseParticipant

class ExpenseParticipantInline(admin.TabularInline):
    model = ExpenseParticipant
    extra = 1
    fields = ('participant', 'contribution')
    readonly_fields = ('contribution',)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', 'type', 'admin', 'created_at')
    list_filter = ('type', 'admin')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'admin', 'type', 'cost')}),
        ('Dates', {'fields': ('created_at',)}),
    )
    inlines = [ExpenseParticipantInline]
    readonly_fields = ('created_at',)
    ordering = ('-created_at', 'title')

class ExpenseParticipantAdmin(admin.ModelAdmin):
    list_display = ('expense', 'participant', 'contribution')
    list_filter = ('expense', 'participant')
    search_fields = ('participant__email', 'expense__title')
    readonly_fields = ('contribution',)
    ordering = ('-expense',)

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseParticipant, ExpenseParticipantAdmin)