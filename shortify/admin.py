from django.contrib import admin
import socket
from .models import *

# Register your models here.


@admin.register(UserPhoneNumber)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user" , "phone")
    list_display_links = list_display[:]


@admin.register(UserURL)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user" , "hash_text" , "url", "date")
    list_display_links = list_display[:]

    def date(selfs , object):
        return datetime.strftime(object.date_added, '%a %d %b %Y %I:%M %p %Z')


@admin.register(AnonymousURL)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ( "hash_text" , "url", "date")
    list_display_links = list_display[:]

    def date(selfs , object):
        return datetime.strftime(object.date_added, '%a %d %b %Y %I:%M %p %Z')


@admin.register(UserURLStatistics)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user" , "show_url" , "date")
    list_filter = [ "user", "date_clicked" ]
    list_display_links = list_display[:]
    
    def show_url(self , object):
        return object.url.url
    
    def date(selfs , object):
        return datetime.strftime(object.date_clicked, '%a %d %b %Y %I:%M %p %Z')



admin.site.site_title = 'kutt Admin Panel'
admin.site.site_header = 'Kutt Admin Panel'
admin.site.index_title = 'Welcome to kutt'