from django.urls import path

from users.views import UserLoginView, UserRegistrationView, UserLogoutView, verify, profile
# from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
    path('profile/', profile, name='profile'),
    # path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    # path('edit/', edit, name='edit'),
]
