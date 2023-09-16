from django.contrib import admin
from . models import User_Follow,Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(User_Follow)

class Change_User_ModelInline(admin.StackedInline) : # class name_Inline(admin.StackInline/admin.TabularInline)

    model = Profile
    can_delete = False

class ExtendedUserAmin(UserAdmin) :

    inlines = (Change_User_ModelInline,)

admin.site.unregister(User)
admin.site.register(User,ExtendedUserAmin)