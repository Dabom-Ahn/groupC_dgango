from django.shortcuts import render
from post_app.models import Post
from post_app.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

# 게시글 목록 조회(GET), 게시글 작성(POST)
@api_view(['GET', 'POST'])
def posts(request):
    if request.method == 'GET':
        # 쿼리 파라미터에서 카테고리와 검색어 가져오기
        category = request.query_params.get('category', None)
        query = request.query_params.get('query', None)
        
        # 기본 쿼리셋 설정 후 조건에 따라 필터링
        posts = Post.objects.all()
        if category:
            posts = posts.filter(category=category.upper())
        if query:
            posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))
        
        # 최신 순으로 정렬하여 상위 3개 항목 반환
        posts = posts.order_by('-created')[:3]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세 조회, 수정(PUT), 삭제(DELETE)
@api_view(['GET', 'PUT', 'DELETE'])
def posts_detail(request, slug): 
    try:
        post = Post.objects.get(slug=slug)  
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 검색 기능
@api_view(['GET'])
def search_posts(request):
    query = request.query_params.get('query', None)
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response([], status=status.HTTP_200_OK)  # 검색어가 없을 경우 빈 리스트 반환
