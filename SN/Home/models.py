from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model) :

    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='posts')
    post_title = models.CharField(max_length=100,blank=True,null=True)
    post_body = models.TextField()
    slug = models.SlugField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta :
        ordering = ('-create','-update','post_body')

    def __str__(self) :
        return self.slug

    def get_absolute_url(self) :
        return reverse('Home:detail',args=(self.id,self.slug))

    def post_like_count(self) :
        return self.post_likes.count()

    def user_can_like(self,user) :
        user_like = user.user_likes.filter(post=self)
        if user_like.exists() :
            return True
        else :
            return False
class Post_Comment(models.Model) :

    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='user_comments')
    post = models.ForeignKey(to=Post,on_delete=models.CASCADE,related_name='post_comments')
    reply_comment = models.ForeignKey(to='self',on_delete=models.CASCADE,related_name='reply_comments',null=True,blank=True) # The post that we replied on
    is_reply = models.BooleanField(default=False)
    comment_body = models.CharField(max_length=400)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f'{self.user} commented on post of {self.post.user} and comment is {self.comment_body[:10]}'


class Post_Like(models.Model) :

    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='user_likes')
    post = models.ForeignKey(to=Post,on_delete=models.CASCADE,related_name='post_likes')

    def __str__(self) :
        return f'{self.user} liked post {self.post.slug}'