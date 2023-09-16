from .forms import User_RegistrationForm, User_LoginForm,User_ChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from . models import User_Follow
from django.views import View

# Create your views here.
class User_RegistrationView(View) :

    template_name = 'account/Register.html'
    form_class = User_RegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You logged in before , can not access requested page', extra_tags='warning')
            return redirect('Home:home')
        return super().dispatch(request, *args, *kwargs)

    def get(self, request) :
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request) :
        if request.method == 'POST' :
            form = self.form_class(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = User.objects.create_user(cd['user_name'], cd['email'], cd['first_password'])
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                user.save()
                messages.success(request, 'User registered successfully', extra_tags='success')
                messages.info(request, 'Login now to use options', extra_tags='info')
                return redirect('account:login')
            else:
                return render(request, self.template_name, context={'form': form})
        return redirect('Home:home')


class User_LoginView(View):

    template_name = 'account/Login.html'
    form_class = User_LoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next',None)
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You logged in before , can not access requested page', extra_tags='warning')
            return redirect('Home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = User_LoginForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = User_LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request, username=cd['user_name_or_email'], password=cd['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'User logged in successfully', extra_tags='success')
                    if self.next :
                        return redirect(self.next)
                    return redirect('Home:home')
                else:
                    messages.error(request, 'User name / email or password is wrong , try agian', extra_tags='danger')
                    return redirect('account:login')
            else:
                return render(request, self.template_name, context={'form': form})
        return redirect('Home:home')


class User_LogoutView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'To use logout option , you must login first', extra_tags='warning')
            return redirect('account:login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        messages.success(request, 'User logged out successfully', extra_tags='success')
        return redirect('Home:home')


class User_ProfileView(LoginRequiredMixin, View):

    template_name = 'account/Profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'To see profiles , you must login first', extra_tags='warning')
            return redirect('account:login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all() # posts in rn in models
        relation = User_Follow.objects.filter(from_user=request.user,to_user=user)
        if relation.exists() :
            is_following = True
        return render(request, self.template_name, context={'user': user, 'posts': posts,'is_following':is_following})


class Password_ResetView(auth_views.PasswordResetView,View):  # This class make a link and send it to user to change password

    template_name = 'account/Password_Reset_Form.html'  # This form take user email and send a link to it
    success_url = reverse_lazy('account:password_reset_done')  # If everything is ok redirect user ti this page
    email_template_name = 'account/Password_Reset_Email.html'  # Contains the link that we want to send

class Password_Reset_DoneView(auth_views.PasswordResetDoneView,View):  # This class works when previous class works well

    template_name = 'account/Password_Reset_Done.html'  # If everything is ok , user see this success page

class Password_Reset_ConfirmView(auth_views.PasswordResetDoneView,View):  # A form to change password

    template_name = 'account/Password_Reset_Confirm.html'  # The form to change
    success_url = reverse_lazy('account:password_reset_complete')  # If user changed password successfully , will be redirect to this page

class Password_Reset_CompleteView(auth_views.PasswordResetCompleteView, View):

    template_name = 'account/Password_Reset_Complete.html'

class User_FollowView(LoginRequiredMixin,View) :

    def setup(self, request, *args, **kwargs):
        self.user_ins = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        user = self.user_ins
        if request.user.id != user.id  :
            return super().dispatch(request,*args,**kwargs)
        else :
            messages.warning(request,'You can not follow/unfollow your account',extra_tags='success')
            return redirect('account:profile',user.id)
    def get(self,request,*args,**kwargs) :
        user = self.user_ins
        relation = User_Follow.objects.filter(from_user=request.user,to_user=user)
        if relation.exists() :
            messages.warning(request,'You can not follow this user , user has followed before',extra_tags='warning')
        else :
            new_relation = User_Follow(from_user=request.user,to_user=user)
            new_relation.save()
            messages.success(request,'User Followed successfully',extra_tags='success')
        return redirect('account:profile',user.id)


class User_UnfollowView(LoginRequiredMixin,View) :

    def setup(self, request, *args, **kwargs):
        self.user_ins = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        user = self.user_ins
        if user.id != request.user.id:
            return super().dispatch(request, *args,**kwargs)
        else:
            messages.warning(request, 'You can not follow/unfollow your account', 'warning')
            return redirect('account:profile', user.id)
    def get(self,request,*args,**kwargs) :
        user = self.user_ins
        relation = User_Follow.objects.filter(from_user=request.user,to_user=user)
        if relation.exists() :
            relation.delete()
            messages.success(request,'User unfollowed successfully',extra_tags='success')
        else :
            messages.warning(request,'You have not followed this user yet',extra_tags='warning')
        return redirect('account:profile',user.id)


class User_Profile_ChangeView(LoginRequiredMixin,View) :

    template_name = 'account/Edit.html'
    form_class = User_ChangeForm
    def get(self,request) :
        form_ins = request.user.profile
        form = self.form_class(instance=form_ins,initial={'email':request.user.email})
        return render(request,self.template_name,context={'form':form})

    def post(self,request) :
        if request.method == 'POST' :
            form = self.form_class(request.POST,instance=request.user.profile)
            if form.is_valid() :
                cd = form.cleaned_data
                form.save()
                request.user.email = cd['email']
                request.user.save()
                messages.success(request,'Profile modified successfully',extra_tags='success')
                return redirect('account:profile',request.user.id)
        return redirect('Home:home')
