#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *


def profile(request, userid):
    try:
        user = User.objects.get(id=userid)
    except User.DoesNotExist:
        raise Http404
        
    try:
        Friendship.objects.get(src=current_user(request), dst=user)
        nmf = False
    except Friendship.DoesNotExist:
        nmf = True
            
    friends = [f.dst for f in Friendship.objects.filter(src=user)]
    
    content = make_template(
        'profile.html',
        user=user,
        friends=friends,
        notmyfriend=nmf
    )
    
    return main_template(
        request, 
        content, 
        title=user.full_name,
        current=3
    )

