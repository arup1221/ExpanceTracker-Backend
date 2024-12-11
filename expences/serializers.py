from rest_framework import serializers
from .models import Category, Expense, RecurringExpense, Budget

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all()
    )
    user = serializers.StringRelatedField()  # To display user as a string rather than ID

    class Meta:
        model = Expense
        fields = ['id', 'user', 'category', 'title', 'amount', 'date', 'description']
        read_only_fields = ['user', 'date']


class RecurringExpenseSerializer(serializers.ModelSerializer):
    expense = serializers.PrimaryKeyRelatedField(queryset=Expense.objects.all())
    interval = serializers.ChoiceField(choices=[
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly')
    ])
    next_due_date = serializers.DateField()

    class Meta:
        model = RecurringExpense
        fields = ['id', 'expense', 'interval', 'next_due_date']


class BudgetSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all()
    )
    user = serializers.StringRelatedField()  
    amount_spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    remaining_amount = serializers.SerializerMethodField()  # New field

    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'limit', 'start_date', 'end_date', 'amount_spent', 'remaining_amount']
        read_only_fields = ['user', 'amount_spent', 'remaining_amount']

    def get_remaining_amount(self, obj):
        amount_spent = obj.amount_spent()
        remaining_amount = obj.limit - amount_spent
        return f"{remaining_amount:.2f}"

