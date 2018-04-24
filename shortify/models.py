from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AnonymousURL(models.Model):
    url = models.TextField(max_length=10000,blank=False, null=False)
    hash_text = models.TextField(max_length=8, blank=False, null=False)
    date_added = models.DateTimeField()

    def __str__(self):
        return str(self.hash_text)

class UserURL(models.Model):
    url = models.TextField(max_length=10000, blank=False, null=False)
    hash_text = models.TextField(max_length=8, blank=False, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField()

    def __str__(self):
        return str(self.user.username) + "  " + str(self.hash_text)