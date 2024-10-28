from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Post(models.Model):
  CATEGORY = (('STUDY','Study'), ('DAIARY','Diary'), ('COMMON','Common'))
  
  title = models.CharField(max_length=100)
  body = models.TextField()
  slug = models.SlugField(unique=True, blank=True, null=True)
  category = models.CharField(max_length=10, choices=CATEGORY, default='COMMON')
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  

  def __str__(self):
    return self.title
    

  def save(self, *args, **kwargs):  
    # 중첩 조건문 형태
    # 만약 인스턴스에 slug값이 없으면 타이틀값으로 슬러그 생성
    if not self.slug:
      slug_base = slugify(self.title)
      slug = slug_base    

      # 위에서 타이틀로 슬러그가 만들진뒤 해당 슬러그에 매칭되는 모델이 있는지 확인하는 중첩 조건문
      # 위에서 변경한 slug와 동일한 slug의 모델데이터가 있으면 다시 해당 슬러그뒤에 고유문자를 붙여처 최종 slug설정
      if Post.objects.filter(slug=slug).exists():
        slug = f'{slug_base}-{get_random_string(5)}'  
        self.slug = slug 

    # 조건문 밖에서 실행되는 최종 모델 저장 구문
    # 위에서 조건처리 완료된 최종 모델인스턴스 테이블에 저장
    super(Post, self).save(*args, **kwargs)
    
