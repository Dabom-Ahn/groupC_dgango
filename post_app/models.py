from django.db import models

class Post(models.Model):
  CATEGORY = (('STUDY','Study'), ('DAIARY','Diary'), ('COMMON','Common'))
  
  title = models.CharField(max_length=100)
  body = models.TextField()
  # url상에서 글 상세페이지 접속시 필요한 글 고유문자값 (id로도 활용가능)
  slug = models.SlugField(unique=True)
  # 글 저장시 카테고리 범주 지정항목 (실제 관리자페이지에서 드롭다운 메뉴 형식으로 표현됨, 기본 선택항목은 COMMON으로 지정)
  category = models.CharField(max_length=10, choices=CATEGORY, default='COMMON')
