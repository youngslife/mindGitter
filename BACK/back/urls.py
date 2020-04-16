from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path("api-auth/", include("rest_framework.urls")),
    # login, registration등 path 설정
    path("api/rest-auth/", include("rest_auth.urls")),
    path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
    # 토큰 발급 및 재발급 페이지 설정
    # 토큰발급
    path('api/rest-auth/obtain_token/', obtain_jwt_token, name="obtain-jwt"),
    path('api/rest-auth/refresh_token/', refresh_jwt_token, name="refresh-jwt"),
    
]
