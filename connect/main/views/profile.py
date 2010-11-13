#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *


def profile(request, userid):
    init(request)
    try:
        user = User.objects.get(id=userid)
    except User.DoesNotExist:
        raise Http404
        
    try:
        Friendship.objects.get(src=request.user, dst=user)
        nmf = False
    except Friendship.DoesNotExist:
        nmf = True
            
    friends = [f.dst for f in Friendship.objects.filter(src=user)]
    
    return HttpResponse(make_template(
        request,
        'profile.html',
        user=user,
        friends=friends,
        notmyfriend=nmf,
        title=user.full_name,
        current=3
    ))

def change_status(request):
    init(request)
    
    new_status = request.POST['status']
    request.user.status = new_status
    request.user.save()
    
    return HttpResponseRedirect('/')
