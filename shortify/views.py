from django.shortcuts import render, HttpResponse, Http404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import UserURL,AnonymousURL, UserPhoneNumber
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
    
    url = str(request.POST.get('url'))

    # prepend http:// to the url if not present
    # if 'http://' not in url and 'https://' not in url:
    #     url = 'http://' + url

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



@csrf_exempt
def validate(request):
    
    # if it is not ajax no need of responding
    if not request.is_ajax():
        return render(request,'404.html',{})
    
    # if it is, then
    email = str(request.POST.get('email'))
    phone = str(request.POST.get('phone'))
    username = str(request.POST.get('username'))

    # whether email or username or phone exists
    all_users = User.objects.all()
    all_phone_numbers = UserPhoneNumber.objects.all()

    usernames = [ str(x.username) for x in list(all_users)]
    emails = [ str(x.email) for x in list(all_users)]
    phones = [ str(x.phone) for x in list(all_phone_numbers)]

    response = {}

    if email in emails:
        response['email'] = True
    else:
        response['email'] = False

    if phone in phones:
        response['phone'] = True
    else:
        response['phone'] = False

    if username in usernames:
        response['username'] = True
    else:
        response['username'] = False

    return response


@csrf_exempt
def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {})

    response = validate(request)
    
    if response['email']:
        response = {'status': 404, 'text':'Email Exists'}
        return JsonResponse(response)
    elif response['phone']:
        response = {'status': 404, 'text':'Phone Exists'}
        return JsonResponse(response)
    elif response['username']:
        response = {'status': 404, 'text':'Username Exists'}
        return JsonResponse(response)
    
    # sign up starts
    fname = request.POST.get('first_name')
    lname = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    password = request.POST.get('password')


    print(lname)
    print('%s %s %s %s %s %s'%(fname, lname, username, email, phone, password))
    
    u = User.objects.create_user(first_name = fname, last_name = lname, username = username, email = email, password = password)
    
    if u:
        # success
        p = UserPhoneNumber(user = u, phone = phone)
        if p:
            # completed
            # perform login
            login(request,u)
            response = {'status': 200, 'text':''}
            return JsonResponse(response)
        else:
            response = {'status': 404, 'text':'Something went wrong'}
            return JsonResponse(response)
    else:
        response = {'status': 404, 'text':'Something went wrong'}
        return JsonResponse(response)



@csrf_exempt
def login_user(request):
    if not request.is_ajax():
        return render(request,'login.html',{})
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    status = '' 
    text = ''

    u = authenticate(username = username, password = password)
    
    if u:
        # authentication success
        login(request, u)
        status = '200'
        text = 'You have successfully logged in'
    else:
        status = '404'
        text = 'Username or password incorrect'
    
    response = {'status':status, 'text': text}
    return JsonResponse(response)

    
def logout_user(request):
    logout(request)
    return redirect('/')