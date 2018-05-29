from django.shortcuts import render, HttpResponse, Http404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required
from .models import UserURL,AnonymousURL, UserPhoneNumber, UserURLStatistics
from datetime import datetime
from dateutil import tz
from kutt import settings
import random
import string
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as dt
import re
from .forms import UserEditForm , ImageChangeForm
# Create your views here.

def home(request):
    return render(request,'index.html',{})
@login_required
def profile(request):
    details = UserPhoneNumber.objects.get(user=request.user)

    if request.method == 'POST':
        form = ImageChangeForm(request.POST , request.FILES)

        if form.is_valid():
            details = UserPhoneNumber.objects.get(user=request.user)
            details.image = form.cleaned_data['image']
            details.save()
            return redirect('/profile')
        else:
            return redirect('/statistics')
    form = ImageChangeForm()
    args = {'details': details, 'form': form}

    return render(request,'profile.html',args)

@csrf_exempt
def short(request):
    uri = str(request.build_absolute_uri())
    host = uri.split('/')[2]
    
    if request.method != 'POST':
        return HttpResponse('not found')
        
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
        # get the URL meta data
        title, desc, icon_url = get_data(url)
        # add to the user urls
        u = UserURL.objects.create(url = url, user = user, hash_text = hash_text, page_title = title, page_desc = desc, page_icon_url = icon_url, date_added = datetime.now())
    
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
            row = UserURL.objects.get(hash_text= path, user = user)
            click = UserURLStatistics.objects.create(user = user, url = row, date_clicked = datetime.now())

            row.no_of_clicks += 1
            row.save()
            url = row.url
            if url.startswith('http://') or url.startswith('https://'):
                return redirect(url)
            else:
                return redirect('http://' + url)
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
def EditProfile(request):

    if request.method == 'GET':
        form = UserEditForm()
        args = {'form': form}
        return render(request, 'userchangeform.html', args)


    if not request.is_ajax():
        return render(request,'404.html', {})

    form = UserEditForm(request.POST, instance=request.user)

    if form.is_valid():
        email = str(request.POST.get('email'))
        all_users = User.objects.all()
        emails = [str(x.email) for x in list(all_users)]



        if email in emails:
            response = {'status': 404, 'text': 'Email Exists'}
            return JsonResponse(response)
        else:
            form.save()

            response = {'status': 200, 'text': ''}
            return JsonResponse(response)
    else:
        return render(request , '404.html')


@csrf_exempt
def signup(request):
    

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'signup.html', {'value':True,'value2':False})

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

    u = User.objects.create_user(first_name = fname, last_name = lname, username = username, email = email, password = password)
    
    if u:
        # success
        p = UserPhoneNumber(user = u, phone = phone)
        if p:
            # completed
            # perform login
            #login(request,u)
            p.save()
            #return redirect('/login')
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
    if request.user_agent.os.family == 'Android':
        pass
    
    if  request.method != 'POST':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request,'login.html',{'value2':True,'value':False})

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


@csrf_exempt
def verify(request):
    if not request.is_ajax():
        return render(request, '404.html', {})
    
    if request.method != 'POST' :
        return Http404('Not Found')
    
    if not request.user.is_authenticated:
        return Http404('Not found')

    hash_text = str(request.POST.get('hash'))
    url = str(request.POST.get('url'))

    if not url.startswith('http:') or not url.startswith('https:'):
        url = 'http://' + url

    # get the hostname
    uri = str(request.build_absolute_uri())
    host = uri.split('/')[2]


    # get hashes of all the shortened URLs
    all_user_hashes = [ x.hash_text for x in UserURL.objects.all() ]
    all_anon_hashes = [ x.hash_text for x in AnonymousURL.objects.all() ]

    # get all the URLs which are already shortened by the user
    all_user_urls = [ x.url for x in UserURL.objects.filter(user = request.user) ]


    response = {}
    
    if hash_text in all_user_hashes + all_anon_hashes :
        # requested URL available
        response['status'] = '404'
        response['text'] = 'Tag already in use'
    elif url in all_user_urls:
        hash_text = UserURL.objects.get(user = request.user, url = url).hash_text
        response['status'] = '404'
        response['text'] = 'URL already shortened as ' + host + '/' + hash_text
    else:
        response['status'] = '200'
    
    return JsonResponse(response)

@csrf_exempt
def custom_shorten(request):
    if not request.is_ajax:
        return render(request, '404.html', {})
    
    if request.method != 'POST':
        return Http404('not found')
    
    if not request.user.is_authenticated:
        return Http404('not found')
    
    url = str(request.POST.get('url'))
    hash_text = str(request.POST.get('tag'))

    if len(url) == 0 or len(hash_text) == 0:
        return Http404('invalid url or tag')
    
    if not url.startswith('http:') and not url.startswith('https:'):
        url = 'http://' + url

    print('%s %s'%(url,hash_text))

    response = {}
    # check whether the hash text exists or not
    if UserURL.objects.filter(hash_text = hash_text).exists() or AnonymousURL.objects.filter(hash_text = hash_text).exists():
        response['status'] = 404
        response['text'] = 'Tag exists'
        return JsonResponse(response)
    
    if UserURL.objects.filter(url = url).exists() or AnonymousURL.objects.filter(url = url).exists():
        response['status'] = 404
        response['text'] = 'URL exists'
        return JsonResponse(response)

    # get the meta data of the URL
    title, desc, icon_url = get_data(url)

    u = UserURL.objects.create(user = request.user, url = url, hash_text = hash_text, page_title = title, page_desc = desc, page_icon_url = icon_url, date_added = datetime.now())
    if u:
        # get the hostname
        uri = str(request.build_absolute_uri())
        http = uri.split('/')[0]
        host = uri.split('/')[2]

        response['status'] = 200
        response['text'] = http + '//' + host + '/' + hash_text

        return JsonResponse(response)
    else:
        response['status'] = 404
        return JsonResponse(response)

@login_required
def statistics(request):
    
    return render(request, 'stati.html',{})







def show_stati(request):
    user = request.user

    # if not ajax return 404 page
    # but if it is from android bypass it
    # print(request.user_agent.os.family)
    if request.user_agent.os.family == 'Android':
        pass
    elif not request.is_ajax():
        print('not ajax')
        return render(request, '404.html', {})

    # if not authenticated return 404 page
    if not user.is_authenticated:
        return render(request, '404.html', {})
    
    # get all urls from UserURLs
    all_urls = UserURL.objects.filter(user = user).order_by('-date_added')
    
    
    data = []
    urls = {}

    # get the minified URL statistics
    for url in all_urls:
        # get the detailed statistics
        detail = UserURLStatistics.objects.filter(url = url, user = user)
        dates = detail.values('date_clicked')
        dates = [v['date_clicked'] for v in [value for value in dates]]

        
        # to avoid duplicate dates
        dates = list(set(dates))
        
        # sort by date
        dates = sorted(dates, key = lambda x : x.date())

        # for i in dates:
        #     print(i)
        
        stati_list = []
        for date in dates:
            stati = {}
            print(date)
            min_dt = datetime.combine(date, dt.time.min)
            max_dt = datetime.combine(date, dt.time.max)
            total_clicks = detail.filter(date_clicked__range = (min_dt, max_dt)).count()
            stati['x'] = datetime.strftime(date, '%d %b %Y')
            stati['y'] = total_clicks
            stati_list.append(stati)
        
        # convert date from UTC to Asia/Kolkata
        date = url.date_added
        UTC = tz.gettz('UTC')
        IN = tz.gettz('Asia/Kolkata')

        date.replace(tzinfo = UTC)
        actual_date = date.astimezone(IN)
        
        urls['url'] = url.url
        urls['hash'] = url.hash_text
        urls['date_added'] = datetime.strftime(actual_date, '%a %d %b %Y %I:%M %p')
        urls['clicks'] = url.no_of_clicks
        urls['title'] = url.page_title
        urls['desc'] = url.page_desc
        urls['icon_url'] = url.page_icon_url
        urls['stati'] = stati_list
        data.append(urls)
        urls = {}
    return JsonResponse({'data':data})


def get_data(url):
    if url.startswith('http:') or url.startswith('https:'):
        pass
    else:
        url = 'http://' + url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    metas = soup.find_all('meta')
    desc = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
    title = soup.find_all('title')[0].text
    title = ''.join([i if ord(i) < 128 else ' ' for i in title])  # removing non-ascii chars

    if len(desc) != 0:
        desc = desc[0]
        desc = ''.join([i if ord(i) < 128 else ' ' for i in desc]) # removing non-ascii chars
    else:
        desc = ''
    return title, desc, get_icon_url(url)
    



def get_icon_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_head = soup.findAll(href=re.compile(r'/.a\w+'))
    img_url = ''
    print(all_head)
    for i in all_head:
        strre=re.compile('shortcut icon', re.IGNORECASE)
        m=strre.search(str(i))
        if m:
            print(i)
            img_url = i["href"]
    
    if img_url == '':
        return img_url
    return to_absolute_url(img_url,response.url)


def to_absolute_url(url, origin):
    # to make the url of the icon to absolute
    if url.startswith('http://') or url.startswith('https://'):
        return url
    # removing the trailing ( and initial ) slash if any
    if str(origin)[-1] == '/':
        origin = origin[:-1]
    if str(url)[0] == '/':
        url = url[1:]
    return origin + '/' + url