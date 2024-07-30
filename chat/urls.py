from django.urls import path
from chat import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('chatbot_responses/', views.chatbot_response, name= 'chatbot_response'),
]