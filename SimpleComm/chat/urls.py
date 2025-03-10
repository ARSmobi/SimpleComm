# from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from .views import UserLoginView, UserRegisterView, LogoutView, room

urlpatterns = [
    path('api/', include('chat.api.urls')),
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/confirm/', TemplateView.as_view(template_name='users/logout.html'), name='logout_confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('chat/', TemplateView.as_view(template_name='chat/chat-room.html'), name='chat'),
    path('<str:room_name>/', room, name='room'),
]
