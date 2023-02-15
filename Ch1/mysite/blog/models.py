from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

# publishedManager class is used to filter the posts by status
class publishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status = Post.Status.PUBLISHED)


# Post model
# 
class Post(models.Model):
    # Status choices enum
    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB','Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    #adding one to many relationship between post and user
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE, 
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #apply the status choices to the status field
    status = models.CharField(max_length=2, 
                              choices=Status.choices, 
                              default=Status.DRAFT)


    #adding the publishedManager class to the objects field
    objects = models.Manager()#default manager
    published = publishedManager()#custom manager

    # Meta class is used to order the posts by publish date
    class Meta:
        ordering = ['-publish']

        #indexing the post
        indexes = [
        models.Index(fields=['publish']),
        ]
    
    def __str__(self):
        return self.title