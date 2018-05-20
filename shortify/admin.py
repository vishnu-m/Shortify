from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(UserPhoneNumber)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user" , "phone")

@admin.register(UserURL)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user" , "hash_text" , "url")

@admin.register(AnonymousURL)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ( "hash_text" , "url")

@admin.register(UserURLStatistics)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user" , "show_url" , "date")

    def show_url(self , object):
        return object.url.url
    def date(selfs , object):
        return datetime.strftime(object.date_clicked, '%a %d %b %Y %I:%M %p %Z')



