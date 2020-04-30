from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts'
# /posts/
urlpatterns = [
    path('', views.PostList.as_view(), name='posts_list'),
    path('<int:post_id>/', views.PostDetail.as_view(), name='post_detail'),
    path('<int:post_id>/analyze/', views.PostAnalyze.as_view(), name='post_analyze'),
    # path('tags/', views.TagCloudTV.as_view(), name='tag_cloud'),
        # 태그
    # path('tags/<str:tag>/', views.)
    path('<int:post_id>/comments/', views.CommentList.as_view(), name='comments_list'),
    path('<int:post_id>/comments/<int:comment_id>/', views.CommentDetail.as_view(), name='comments_detail'),
    path('<int:post_id>/tagtest/', views.tagtest, name='tagtest'),
]