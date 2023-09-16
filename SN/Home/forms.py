from django import forms
from . models import Post,Post_Comment

class Update_PostForm(forms.ModelForm) :

    class Meta :
        model = Post
        fields = ('post_body',)

class Create_PostForm(forms.ModelForm) :

    class Meta :
        model = Post
        fields = ('post_body',)
        widgets = {
            'post_body' : forms.Textarea(attrs={'class':'form-control','placeholder':'Please type your post here'})
        }

class Post_CommentForm(forms.ModelForm) :

    class Meta :
        model = Post_Comment
        fields = ('comment_body',)
        widgets = {
            'comment_body' : forms.Textarea(attrs={'class':'form-control','placeholder':'Please enter your comment here'})
        }

class Post_Reply_CommentForm(forms.ModelForm) :

    class Meta :
        model = Post_Comment
        fields = ('comment_body',)
        widgets = {
            'comment_body' : forms.Textarea(attrs={'class':'form-control','placeholder':'Please reply here'})
        }

class Post_SearchForm(forms.Form) :

    search_field = forms.CharField(min_length=1,max_length=100,label='Search ',
                                   widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Search here...'}))