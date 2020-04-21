from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    # path('', views.board, name='board'),
    # path('<int:id>/', views.board_title, name='board')
]