from django.contrib import admin
from . models import Post,Post_Comment,Post_Like

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin) :

    list_display = ('user','slug','create','update')
    search_fields = ('slug',) # Just one
    list_filter = ('create','update')
    prepopulated_fields = {'slug':('post_body',)}
    raw_id_fields = ('user',) # Just one

@admin.register(Post_Comment)
class Post_CommentAmin(admin.ModelAdmin) :

    list_display = ('user','post','create','is_reply')
    raw_id_fields = ('user','post','reply_comment')

@admin.register(Post_Like)
class Post_LikeAdmin(admin.ModelAdmin) :

    list_display = ('user','post')
    raw_id_fields = ('user','post')