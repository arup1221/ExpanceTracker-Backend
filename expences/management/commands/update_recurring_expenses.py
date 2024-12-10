from django.core.management.base import BaseCommand
from expences.models import RecurringExpense

class Command(BaseCommand):
    help = 'Process recurring expenses and update their due dates'

    def handle(self, *args, **kwargs):
        recurring_expenses = RecurringExpense.objects.all()
        for recurring_expense in recurring_expenses:
            self.stdout.write(
                f"Processing Recurring Expense: {recurring_expense.expense.title} (Next Due: {recurring_expense.next_due_date})"
            )
            recurring_expense.update_next_due_date()
        self.stdout.write("All recurring expenses have been processed.")
