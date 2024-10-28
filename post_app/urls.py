from django.urls import path
from .import views

# posts 경로로 url접속시 views.py에 등록된 posts REST응답 함수 매팽
urlpatterns = [
  path('posts', views.posts, name='posts')
]
