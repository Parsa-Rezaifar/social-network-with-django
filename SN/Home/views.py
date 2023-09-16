from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from . models import Post,Post_Comment,Post_Like
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from . forms import Update_PostForm,Create_PostForm,Post_CommentForm,Post_Reply_CommentForm,Post_SearchForm
from django.utils.text import slugify
from  django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class Home_PageView(View) :

    template_name = 'Home/Home_Page.html'
    form_class = Post_SearchForm

    def get(self,request) :
        posts = Post.objects.all()
        search_form = Post_SearchForm()
        if request.GET.get('search_field') :
            posts = posts.filter(post_body__contains=request.GET['search_field'])
            if not posts.exists() :
                messages.error(request,'search not found',extra_tags='danger')
                return redirect('Home:home')
        return render(request,self.template_name,context={'posts':posts,'search_form':search_form})

class Post_DetailView(LoginRequiredMixin,View) :

    template_name = 'Home/Detail.html'
    form_class = Post_CommentForm
    reply_form_class = Post_Reply_CommentForm

    def setup(self, request, *args, **kwargs):
        self.post_comment_ins = get_object_or_404(Post,pk=kwargs['post_id'],slug=kwargs['post_slug'])
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated :
            messages.warning(request,'To access detail page , you must login first',extra_tags='warning')
            return redirect('account:login')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,post_id,post_slug) :
        form = self.form_class()
        post = get_object_or_404(Post,pk=post_id,slug=post_slug)
        post_comments = self.post_comment_ins.post_comments.filter(is_reply=False)
        can_like = False
        if request.user.id != post.user.id and post.user_can_like(request.user) :
            can_like = True
        return render(request,self.template_name,
                      context={'post':post,'post_comments':post_comments,'form':form,'reply_form':self.reply_form_class,'can_like':can_like})

    @method_decorator(login_required)
    def post(self,request,*args,**kwargs) :
        if request.method == 'POST' :
            form = self.form_class(request.POST)
            if form.is_valid() :
                new_post_comment = form.save(commit=False)
                new_post_comment.user = request.user
                new_post_comment.post = self.post_comment_ins
                new_post_comment.save()
                messages.success(request,'You commented successfully',extra_tags='success')
                return redirect('Home:detail',new_post_comment.post.id,new_post_comment.post.slug)
            else :
                return render(request,self.template_name,context={'form':form})

class Delete_PostView(LoginRequiredMixin,View) :
    def get(self,request,post_id) :
        post = get_object_or_404(Post,pk=post_id)
        if post.user.id == request.user.id :
            post.delete()
            messages.success(request,'Post deleted successfully',extra_tags='success')
            return redirect('account:profile',post.user.id)
        else :
            messages.warning(request,'Only the owner of this profile can delete posts',extra_tags='warning')
            return redirect('Home:home')

class Update_PostView(LoginRequiredMixin,View) :

    template_name = 'Home/Update.html'
    form_class = Update_PostForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id :
            messages.warning(request,'Only the owner of this profile can update posts')
            return redirect('Home:home')
        return super().dispatch(request,*args,**kwargs)
    def get(self,request,*args,**kwargs) :
        update_ins = self.post_instance
        form = Update_PostForm(instance=update_ins)
        return render(request,self.template_name,context={'form':form})

    def post(self,request,*args,**kwargs):
        post = self.post_instance
        update_ins = self.post_instance
        if request.method == 'POST' :
            form = Update_PostForm(request.POST,instance=update_ins)
            if form.is_valid() :
                cd = form.cleaned_data
                new_post_body = form.save(commit=False)
                new_post_body.slug = slugify(cd['post_body'][:30])
                new_post_body.save()
                messages.success(request,'Post updated successfully',extra_tags='success')
                return redirect('Home:detail',post.id,post.slug)

class Create_PostView(LoginRequiredMixin,View) :

    template_name = 'Home/Create.html'
    form_class = Create_PostForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id :
            messages.warning(request,'Only the owner of this profile can create a new post , you must login first',extra_tags='warning')
            return redirect('Home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,context={'form':form})

    def post(self,request):
        if request.method == 'POST' :
            form = self.form_class(request.POST)
            if form.is_valid() :
                cd = form.cleaned_data
                new_post = form.save(commit=False)
                new_post.slug = slugify(cd['post_body'][:30])
                new_post.user = request.user
                new_post.save()
                messages.success(request,'New post created successfully',extra_tags='success')
                return redirect('account:profile',request.user.id)

class Reply_CommentView(LoginRequiredMixin,View) :

    reply_form_class = Post_Reply_CommentForm

    def setup(self, request, *args, **kwargs) :
        self.comment_ins = get_object_or_404(Post_Comment,pk=kwargs['comment_id'])
        self.post_ins = get_object_or_404(Post,pk=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)
    
    def dispatch(self, request, *args, **kwargs) :
        comment = self.comment_ins
        post = self.post_ins
        if post.user.id == comment.user.id :
            messages.warning(request,'You can not use this option to your posts',extra_tags='warning')
            return redirect('Home:home')
        return super().dispatch(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs) :
        if request.method == 'POST' :
            post = self.post_ins
            reply_comment = self.comment_ins
            form = self.reply_form_class(request.POST)
            if form.is_valid() :
                reply_post = form.save(commit=False)
                reply_post.user = request.user
                reply_post.post = post
                reply_post.reply_comment = reply_comment
                reply_post.is_reply = True
                reply_post.save()
                messages.success(request,'Replied successfully',extra_tags='success')
            return redirect('Home:detail',post.id,post.slug)

class Post_LikeView(LoginRequiredMixin,View) :

    def get(self,request,*args,**kwargs):
        post = get_object_or_404(Post,pk=kwargs['post_id'])
        like_relation = Post_Like.objects.filter(user=request.user,post=post)
        if like_relation.exists() :
            messages.warning(request,'You can not like this post , liked before',extra_tags='warning')
            return redirect('Home:detail',post.id,post.slug)
        else :
            Post_Like.objects.create(user=request.user,post=post).save()
            messages.success(request,'Post liked successfully',extra_tags='success')
            return redirect('Home:detail',post.id,post.slug)