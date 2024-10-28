from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Post(models.Model):
  CATEGORY = (('STUDY','Study'), ('DAIARY','Diary'), ('COMMON','Common'))
  
  title = models.CharField(max_length=100)
  body = models.TextField()
  # url상에서 글 상세페이지 접속시 필요한 글 고유문자값 (id로도 활용가능)
  slug = models.SlugField(unique=True)
  # 글 저장시 카테고리 범주 지정항목 (실제 관리자페이지에서 드롭다운 메뉴 형식으로 표현됨, 기본 선택항목은 COMMON으로 지정)
  category = models.CharField(max_length=10, choices=CATEGORY, default='COMMON')
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  # Post 클래스에서 생성되는 인스턴스 모델의 타이틀 값을 문자열로 반환
  def __str__(self):
    return self.title
  
  # 해당 클래스가 생성하는 모델 인스턴스르 저장해주는 함수
  def save(self, *args, **kwargs):
    # 모델 인스턴스 생성시 slug항목이 없으면 제목값을 슬러그화해서 대신 저장
    if not self.slug:
      slug_base = slugify(self.title)
      slug = slug_base
    
    # 이미 DB상의 같은 항목의 slug 게시글이 존재하면
    # 기존 slug이름에 랜덤한 5글자의 고유 문자값을 적용하여 slug 중복피함
    if Post.objects.filter(slug=slug).exists():
      slug = f'{slug_base}-{get_random_string(5)}'
    # 위의 조건문으로 중복회피한 새로운 슬러그를 인스턴에스 적용
    self.slug = slugify
    
    #부모 클래스의 save함수를 super를 이용하여 위의 적용내용들을 반환해서 호출 및 저장
    super(Post, self).save(*args, **kwargs)
    
