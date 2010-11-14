#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *

def friends(request):
    if not init(request):
        return HttpResponseRedirect('/login')
    cu = request.user
    notify = None
    friends = []
    requests = []

    if request.GET:
        if 'delete' in request.GET:
            user = User.objects.get(id=request.GET['delete'])
            notify = u'%s удален из друзей' % user.full_name
            try:
                Friendship.objects.get(src=cu, dst=user).delete()
            except Friendship.DoesNotExist:
                pass
            try:
                Friendship.objects.get(src=user, dst=cu).delete()
            except Friendship.DoesNotExist:
                pass
        if 'add' in request.GET:
            user = User.objects.get(id=request.GET['add'])
            notify = u'Запрос дружбы отправлен'
            try:
                Friendship.objects.get(src=cu, dst=user)
            except Friendship.DoesNotExist:
                Friendship(src=cu, dst=user).save()
        if 'accept' in request.GET:
            user = User.objects.get(id=request.GET['accept'])
            notify = u'Добавлен друг: %s' % user.full_name
            try:
                Friendship.objects.get(src=cu, dst=user)
            except Friendship.DoesNotExist:
                Friendship(src=cu, dst=user).save()
                
    for fs in Friendship.objects.filter(dst=cu):
        friends.append(fs.src)
        fs.src.is_my_request = False
        try:
            Friendship.objects.get(src=cu, dst=fs.src)
            fs.src.is_request = False
        except Friendship.DoesNotExist:
            fs.src.is_request = True
            
    for fs in Friendship.objects.filter(src=cu):
        if not fs.dst in friends:
            friends.append(fs.dst)
            fs.dst.is_request = False
            fs.dst.is_my_request = True

    friends = sorted(friends, key=lambda f: f.surname)
    friends = sorted(friends, key=
        lambda f: 
            (-10 if f.is_request else 0) +
            (-1 if f.is_my_request else 0)
    )
    
    return HttpResponse(make_template(
        request, 
        'friends.html',
        friends=friends,
        requests=requests,
        notification=notify, 
        title='Друзья',
        current=3
    ))
    
