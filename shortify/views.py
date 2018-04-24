from django.shortcuts import render, HttpResponse, Http404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import UserURL,AnonymousURL
from datetime import datetime
from kutt import settings
import random
import string
import re

# Create your views here.

def home(request):
    return render(request,'index.html',{})

@csrf_exempt
def short(request):
    uri = str(request.build_absolute_uri())
    host = uri.split('/')[2]
    print(host)
    url = str(request.POST.get('url'))
    
    # prepend http:// to the url if not present
    if 'http://' not in url and 'https://' not in url:
        url = 'http://' + url

    # get the user
    user = request.user

    # check whether the url already added 
    if request.user.is_authenticated:
        # in the case of registered users
        is_existing = UserURL.objects.filter(url=url).exists()
        if is_existing:
            row = UserURL.objects.get(url=url)
            if row.user.username == user.username:
                hash_text = row.hash_text
                short_url = 'http://' + host + "/" + hash_text
                return HttpResponse(short_url)
    else:
        is_existing = AnonymousURL.objects.filter(url=url).exists()
        if is_existing:
            hash_text = AnonymousURL.objects.get(url=url).hash_text
            short_url = 'http://' + host + "/" + hash_text
            return HttpResponse(short_url)
        
    
        
            
    # create a hash
    hash_text = generate_hash()

    short_url = 'http://' + host + "/" + hash_text


    # add the url to the database
    if user is None or user.username == '':
        '''add to anonymouse urls'''
        u = AnonymousURL.objects.create(url=url, hash_text = hash_text, date_added = datetime.now())
    else:
        # add to the user urls
        u = UserURL.objects.create(url = url, user = user, hash_text = hash_text, date_added = datetime.now())
    
    if u:
        return HttpResponse(short_url)
    else:
        return Http404("Something went wrong")   


    return HttpResponse(text)

def get_url(request):
    path = str(request.path)
    
    # removing the slashes
    path = path[1:-1]

    user = request.user
    # get the url corresponding to the hash
    if user.is_authenticated:
        row = UserURL.objects.filter(hash_text= path, user = user)
        if row.exists():
            return redirect(row[0].url)
    else:
        row = AnonymousURL.objects.filter(hash_text= path)
        if row.exists():
            return redirect(row[0].url)       

    return render(request,'404.html',{})

def generate_hash():
    p = string.ascii_letters + string.digits + '_'
    hash_text = "".join(random.choice(p) for i in range(settings.URL_HASH_SIZE))
    objects = list(AnonymousURL.objects.filter()) + list(UserURL.objects.filter())
    used_hashes = [x.url.split("/")[-1] for x in objects]
    if hash_text in used_hashes:
        return generate_hash()
    else:
        return hash_text