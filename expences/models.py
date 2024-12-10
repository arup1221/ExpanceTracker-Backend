from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db import transaction

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount} by {self.user.username}"

###########################################################################################################################
# no need to use it now
class RecurringExpense(models.Model):
    expense = models.OneToOneField('Expense', on_delete=models.CASCADE)
    interval = models.CharField(
        max_length=20,
        choices=[
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly'),
            ('Monthly', 'Monthly'),
            ('Yearly', 'Yearly')
        ]
    )
    next_due_date = models.DateField()

    def update_next_due_date(self):
        
        today = timezone.now().date()
        
        with transaction.atomic():  # Ensure atomicity
            while self.next_due_date <= today:
                Expense.objects.create(
                    user=self.expense.user,
                    category=self.expense.category,
                    title=f"{self.expense.title} (Recurring)",
                    amount=self.expense.amount,
                    date=self.next_due_date,
                    description=self.expense.description
                )

                if self.interval == 'Daily':
                    self.next_due_date += timedelta(days=1)
                elif self.interval == 'Weekly':
                    self.next_due_date += timedelta(weeks=1)
                elif self.interval == 'Monthly':
                    self.next_due_date += relativedelta(months=1)
                elif self.interval == 'Yearly':
                    self.next_due_date += relativedelta(years=1)
            
            self.save()

    def __str__(self):
        return f"Recurring {self.expense.title} - {self.interval}"
###########################################################################################################################
class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def amount_spent(self):
        return Expense.objects.filter(
            user=self.user,
            category=self.category,
            date__range=(self.start_date, self.end_date)
        ).aggregate(total_spent=Sum('amount'))['total_spent'] or 0

    def __str__(self):
        return f"{self.category.name} Budget - {self.user.username}"
