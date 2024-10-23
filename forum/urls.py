from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topic/new/', views.create_topic, name='create_topic'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topic/<int:pk>/edit/', views.update_topic, name='update_topic'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
