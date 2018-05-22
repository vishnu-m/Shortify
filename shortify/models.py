from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class AnonymousURL(models.Model):
    url = models.TextField(max_length=10000,blank=False, null=False)
    hash_text = models.TextField(max_length=8, blank=False, null=False)
    date_added = models.DateTimeField()

    def __str__(self):
        return str(self.hash_text) +  "  " + str(self.url)

class UserURL(models.Model):
    url = models.TextField(max_length=10000, blank=False, null=False)
    hash_text = models.TextField(max_length=8, blank=False, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    no_of_clicks = models.PositiveIntegerField(default = 0, blank=False, null=False)
    page_title = models.TextField(default='',max_length=10000, blank= False, null=False)
    page_desc = models.TextField(default='',max_length=10000, blank=False, null=False)
    page_icon_url = models.TextField(default='',max_length=10000, blank=False, null=False)
    date_added = models.DateTimeField()



class UserPhoneNumber(models.Model):
    user = models.OneToOneField(to = User, on_delete = models.CASCADE)
    phone = models.TextField(max_length=13, blank=False, null=False )

    def __str__(self):
        return  self.phone



# on each click a new row wil be added here
class UserURLStatistics(models.Model):
    user = models.ForeignKey(to = User, on_delete = models.CASCADE)
    url = models.ForeignKey(to = UserURL, on_delete = models.CASCADE);
    date_clicked= models.DateTimeField()


    class Meta:
        verbose_name = 'User URL Statistics'
        verbose_name_plural = verbose_name
