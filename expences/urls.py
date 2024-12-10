from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ExpenseViewSet, BudgetViewSet, SummaryAPIView, MonthlyHistoryView, YearlyHistoryView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'expenses', ExpenseViewSet, basename='expense')
# router.register(r'recurring-expenses', RecurringExpenseViewSet, basename='recurringexpense')
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path('', include(router.urls)),
    # path('recurring-expenses/<int:pk>/update-next-due-date/',UpdateNextDueDateView.as_view(), name='update-next-due-date'),
    path('summary/', SummaryAPIView.as_view(), name='expense-summary'),
    path('monthly-history/', MonthlyHistoryView.as_view(), name='monthly-history'),
    path('yearly-history/', YearlyHistoryView.as_view(), name='yearly-history'),
]
