from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post  # 사용할 모델을 지정
        fields = ['title', 'body', 'slug', 'category', 'created', 'updated', 'link']  # 직렬화할 필드 목록
