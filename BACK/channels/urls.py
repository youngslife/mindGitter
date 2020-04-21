from django.urls import path
from . import views

app_name = 'channels'

urlpatterns = [
    path('', views.board, name='board'),
    path('<int:id>/', views.board_title, name='board_title'),
    path('join/<int:id>/', views.board_join, name='board_join'),
]