from django.urls import path
from . import views

app_name = 'user_profile'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/<int:pk>/', views.view_profile, name="profile_view"),
]