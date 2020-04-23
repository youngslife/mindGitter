from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts'
# /posts/
urlpatterns = [
    path('', views.PostList.as_view(), name='posts_list'),
    path('<int:post_id>/', views.PostDetail.as_view(), name='post_detail'),
    # path('tags/', views.TagCloudTV.as_view(), name='tag_cloud'),
        # 태그
    # path('tags/<str:tag>/', views.)
    # path('<int:post_id>/comments/', views.comments_list, name='comments_list')
]