from django.template import Context, loader
from django.http import HttpResponse
from models import *
import settings
import os
import Image


def login_user(request, user):
    request.session['user'] = user
    
def current_user(request):
    return User.objects.get(email=request.session['user'])

def logged_in(request):
    return 'user' in request.session
    
def main_template(request, content, current=1, title='', notification=None, error=None):
    t = loader.get_template('main.html')
    c = Context({
        'page_title': title + ' | Connect',
        'content': content,
        'has_menu': True,
        'current': current,
        'error': error,
        'notification': notification,
        'friend_request_count': friend_request_count(request),
        'unread_messages_count': unread_messages_count(request),
        'days': range(1,32),
        'months': range(1,13),
        'years': xrange(2010,1970,-1),
        'langs': Language.objects.all(),
        'me': current_user(request),
    })
    return HttpResponse(t.render(c))
    
def make_template(template, **kwargs):
    t = loader.get_template(template)
    c = Context(kwargs)
    return t.render(c)
    
def make_paginator(l, pl, st, link):
    return make_template(
            'paginator.html',
            pages=range(1,(l+pl-1)/pl+1),
            link=link,
            current=st/pl+1
        )
           
def download_file(file, *path):
    srcf = os.path.join(settings.STORAGE_PATH, *path)
    open(srcf, 'w').write(file.read())
    return srcf

def resize_image(file, size, path):
    img = Image.open(file)
    img.thumbnail((size, size), Image.ANTIALIAS)
    img.save(path)

def unread_messages_count(request):
    cu = current_user(request)
    c = len(Message.objects.filter(owner=cu, unread=1))
    return c if c > 0 else ''

def friend_request_count(request):
    c = 0
    cu = current_user(request)
    for fs in Friendship.objects.filter(dst=cu):
        try:
            Friendship.objects.get(src=cu, dst=fs.src)
        except Friendship.DoesNotExist:
            c += 1
    return c if c > 0 else ''
    
def delete_avatar(user):
    if user.avatar != 'default.png':
        try:
            os.unlink(os.path.join(settings.STORAGE_PATH, 'avatars', '100.' + user.avatar))
            os.unlink(os.path.join(settings.STORAGE_PATH, 'avatars', '50.' + user.avatar))
            os.unlink(os.path.join(settings.STORAGE_PATH, 'avatars', '25.' + user.avatar))
        except:
            pass
    user.avatar = 'default.png'
    user.save()
        
def save_avatar(request, user):
    delete_avatar(user)
    f = request.FILES['avatar']
    ext = f.name.split('.')[-1]
    fn = str(user.id) + '.' + ext
    srcf = download_file(f, 'avatars',  fn)
    resize_image(
        srcf,
        100,
        os.path.join(settings.STORAGE_PATH, 'avatars', '100.'+fn)
    )
    resize_image(
        srcf,
        50,
        os.path.join(settings.STORAGE_PATH, 'avatars', '50.'+fn)
    )
    resize_image(
        srcf,
        25,
        os.path.join(settings.STORAGE_PATH, 'avatars', '25.'+fn)
    )
    os.unlink(srcf)
    user.avatar = fn

