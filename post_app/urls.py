from django.urls import path
from .import views

# posts 경로로 url접속시 views.py에 등록된 posts REST응답 함수 맵핑
urlpatterns = [
  path('posts', views.posts, name='posts'),
  path('api/posts/', views.posts, name='posts'),
  path('api/search', views.search_posts, name='search_posts'),  # 검색 API 추가
]
