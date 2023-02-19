from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
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
    slug = models.SlugField(max_length=250, unique_for_date='publish')
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
    
    def __len__(self):
        return len(self.body)
    
    #get_absolute_url method is used to redirect to the post detail page
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
    


# Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE, 
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'