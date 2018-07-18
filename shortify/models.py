from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

def get_user_fullname( self ):
    full_name = self.first_name + ' ' + self.last_name
    if full_name.strip() == '':
        full_name = self.username
    return full_name

User.add_to_class( "__str__", get_user_fullname)



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

    def __str__( self ):
        return str( self.user ) + ' ' + str( self.url )


class UserPhoneNumber(models.Model):
    user = models.OneToOneField(to = User, on_delete = models.CASCADE)
    phone = models.TextField(max_length=13, blank=False, null=False )



# on each click a new row wil be added here
class UserURLStatistics(models.Model):
    user = models.ForeignKey(to = User, on_delete = models.CASCADE)
    url = models.ForeignKey(to = UserURL, on_delete = models.CASCADE);
    date_clicked= models.DateTimeField( auto_now_add = True )


    class Meta:
        verbose_name = 'User URL Statistics'
        verbose_name_plural = verbose_name
