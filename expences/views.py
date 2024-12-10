from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Category, Expense, RecurringExpense, Budget
from .serializers import CategorySerializer, ExpenseSerializer, RecurringExpenseSerializer, BudgetSerializer
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from django.db.models import Sum
from dateutil.relativedelta import relativedelta

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]



class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# class RecurringExpenseViewSet(viewsets.ModelViewSet):
#     serializer_class = RecurringExpenseSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return RecurringExpense.objects.filter(expense__user=self.request.user)

#     def perform_create(self, serializer):
#         expense_id = self.request.data.get('expense_id')
#         if not expense_id:
#             raise ValidationError({"detail": "Expense ID is required."})
        
#         # Fetch the expense and check user ownership
#         expense = get_object_or_404(Expense, id=expense_id, user=self.request.user)
        
#         # Save the serializer with the expense instance
#         serializer.save(expense=expense)
        
        
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.update_next_due_date()  # Update the due date based on the interval
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)



class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# class UpdateNextDueDateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         recurring_expense = RecurringExpense.objects.filter(id=pk, expense__user=request.user).first()
#         if recurring_expense:
#             recurring_expense.update_next_due_date()
#             serializer = RecurringExpenseSerializer(recurring_expense)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({"detail": "Recurring expense not found"}, status=status.HTTP_404_NOT_FOUND)


class SummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        today = date.today()
        
        total_expense = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        
        today_expense = self.get_total_for_range(user, today, today)
        
        last_day_expense = self.get_total_for_range(user, today - timedelta(days=1), today-timedelta(days=1))
        
        current_week_expense = self.get_total_for_range(user, today - timedelta(days=today.weekday()), today)
        
        last_week_expense = self.get_total_for_range(user, today - timedelta(days=today.weekday() + 7), today - timedelta(days=today.weekday() + 1))
        
        current_month_expense = self.get_total_for_range(user, today.replace(day=1), today)
        
        last_month_expense = self.get_total_for_range(user, (today.replace(day=1) - timedelta(days=1)).replace(day=1), today.replace(day=1) - timedelta(days=1))
        
        current_year_expense = self.get_total_for_range(user, today.replace(month=1, day=1), today)
        
        last_year_expense = self.get_total_for_range(user, today.replace(year=today.year - 1, month=1, day=1), today.replace(year=today.year - 1, month=12, day=31))

        summary = {
            "total_expense": total_expense,
            "today_expense":today_expense,
            "last_day_expense":last_day_expense,
            "current_week_expense": current_week_expense,
            "last_week_expense": last_week_expense,
            "current_month_expense": current_month_expense,
            "last_month_expense": last_month_expense,
            "current_year_expense": current_year_expense,
            "last_year_expense": last_year_expense,
        }

        return Response(summary)
    
    def get_total_for_range(self, user, start_date, end_date):
        # Sum non-recurring expenses
        expense_total = Expense.objects.filter(user=user, date__range=(start_date, end_date)).aggregate(Sum('amount'))['amount__sum'] or 0

        # Comment out the part related to recurring expenses
        # recurring_expenses = RecurringExpense.objects.filter(expense__user=user)
        # for recurring in recurring_expenses:
        #     expense_total += self.calculate_recurring_amount(recurring, start_date, end_date)

        return expense_total

    # Commenting out the recurring expense logic
    # def calculate_recurring_amount(self, recurring, start_date, end_date):
    #     """Calculate the total for recurring expenses within a date range."""
    #     total = 0
    #     date = recurring.next_due_date
    #     interval_days = {
    #         'Daily': timedelta(days=1),
    #         'Weekly': timedelta(weeks=1),
    #         'Monthly': relativedelta(months=1),
    #         'Yearly': relativedelta(years=1),
    #     }
        
    #     interval = interval_days[recurring.interval]

    #     # Generate expense instances within the date range
    #     while date <= end_date:
    #         if date >= start_date:
    #             total += recurring.expense.amount
    #         date += interval

    #     return total


class MonthlyHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        months = int(request.query_params.get("months", 12))  # Default: Last 3 months
        history = []

        for i in range(months):
            month_start = (timezone.now() - relativedelta(months=i)).replace(day=1)
            month_end = (month_start + relativedelta(months=1)) - timedelta(days=1)

            # Fetch regular expenses
            regular_expenses = Expense.objects.filter(
                user=user,
                date__range=(month_start, month_end)
            ).aggregate(total=Sum('amount'))['total'] or 0

            # Commenting out recurring expenses logic
            # recurring_expenses = RecurringExpense.objects.filter(
            #     expense__user=user,
            #     next_due_date__range=(month_start, month_end)
            # ).aggregate(total=Sum(F('expense__amount')))['total'] or 0

            history.append({
                "month": month_start.strftime("%B %Y"),
                "regular_expenses": regular_expenses,
                # Commenting out recurring expenses part
                # "recurring_expenses": recurring_expenses,
                "total_expenses": regular_expenses,  # Only regular expenses
            })

        return Response(history, status=200)


class YearlyHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        years = int(request.query_params.get("years", 5))  # Default: Last 3 years
        history = []

        for i in range(years):
            year_start = (timezone.now() - relativedelta(years=i)).replace(month=1, day=1)
            year_end = (year_start + relativedelta(years=1)) - timedelta(days=1)

            # Fetch regular expenses
            regular_expenses = Expense.objects.filter(
                user=user,
                date__range=(year_start, year_end)
            ).aggregate(total=Sum('amount'))['total'] or 0

            # Commenting out recurring expenses logic
            # recurring_expenses = RecurringExpense.objects.filter(
            #     expense__user=user,
            #     next_due_date__range=(year_start, year_end)
            # ).aggregate(total=Sum(F('expense__amount')))['total'] or 0

            history.append({
                "year": year_start.year,
                "regular_expenses": regular_expenses,
                # Commenting out recurring expenses part
                # "recurring_expenses": recurring_expenses,
                "total_expenses": regular_expenses,  # Only regular expenses
            })

        return Response(history, status=200)
