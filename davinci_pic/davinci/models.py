from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class USER_DATA(models.Model):
    user_id = models.ForeignKey(User,default=1, on_delete=models.CASCADE,)
    username = models.CharField(max_length=264)
    login_count = models.PositiveIntegerField(null = True)
    email = models.EmailField(null = True,blank= True)
    first_name = models.CharField(null = True,blank= True, max_length = 264)
    last_name = models.CharField(null = True,blank= True, max_length = 264)
    country_code = models.PositiveIntegerField(null = True)
    mobile_number = models.BigIntegerField(null = True)
    
    def __str__(self):
        return self.username

class folder_files_model(models.Model):
    user_id = models.ForeignKey(User,default=1, on_delete=models.CASCADE,)
    username = models.CharField(max_length=264)
    folder_count = models.PositiveIntegerField(null = True)
    files_count = models.PositiveIntegerField(null = True)

    def __str__(self):
        return self.username

