from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LogoutView, UserDetailsAPI # UserDetailsViewSet

# router = DefaultRouter()
# router.register(r'user-details', UserDetailsViewSet, basename='user-details')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('', include(router.urls)),
    path('user-details/', UserDetailsAPI.as_view(), name='user-details'),
]
