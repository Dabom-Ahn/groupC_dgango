from django.shortcuts import render
from post_app.models import Post
from post_app.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

@api_view(['GET', 'POST'])
def posts(request):
    # GET 방식 요청이 들어왔을 때 응답 처리
    if request.method == 'GET':
        # 요청 URL에 category와 query 쿼리 파라미터가 있는지 확인
        category = request.query_params.get('category', None)
        query = request.query_params.get('query', None)

        # 기본 쿼리셋 설정
        posts = Post.objects.all()

        # category 파라미터가 있는 경우 필터링
        if category:
            posts = posts.filter(category=category.upper())

        # query 파라미터가 있는 경우 제목과 본문에 검색어가 포함된 항목 필터링
        if query:
            posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))

        # 최신 순으로 정렬하여 상위 3개 항목 반환
        posts = posts.order_by('-created')[:3]

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # POST 방식 요청이 들어왔을 때 응답 처리
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_posts(request):
    query = request.query_params.get('query', None)  # 검색어 가져오기
    if query:
        # title 또는 body에 검색어가 포함된 게시물 필터링
        posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    return Response([])  # 검색어가 없을 경우 빈 리스트 반환