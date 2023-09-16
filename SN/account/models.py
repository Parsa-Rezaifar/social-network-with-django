from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_Follow(models.Model) :

    from_user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='followers')
    to_user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='followings')
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self) :

        return f'{self.from_user} followed {self.to_user}'

class Profile(models.Model) :

    user = models.OneToOneField(to=User,on_delete=models.CASCADE) #one to one do not need related_name
    user_age = models.PositiveBigIntegerField(default=0)
    user_bio = models.TextField(blank=True,null=True)

