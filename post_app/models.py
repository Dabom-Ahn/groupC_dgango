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
    slug= ''
    if not self.slug:
      slug_base = slugify(self.title)
      slug = slug_base    

    
    if Post.objects.filter(slug=slug).exists():
      slug = f'{slug_base}-{get_random_string(5)}'     

    self.slug = slug    
    super(Post, self).save(*args, **kwargs)
    
