#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from datetime import *


def viewmsg(request, id):
    init(request)
    cu = request.user
    notify = None
    senders = []
    
    user = User.objects.get(id=id)
    msgs = []
    msgs.extend(Message.objects.filter(src=user, owner=cu))
    msgs.extend(Message.objects.filter(dst=user, owner=cu))
    msgs = sorted(msgs, key=lambda x: x.date)
    msgs = [m for m in reversed(msgs)]
    
    try:
        st = int(request.GET['page'])*10-10
    except:
        st = 0
    
    for m in msgs:
        if m.unread == 1:
            m.unread = 0
            m.save()
                    
    return HttpResponse(make_template(
        request, 
        'messages-view.html',
        title='Сообщения',
        current=2,
        u=user,
        messages=msgs[st:st+10],
        pager=make_paginator(
            request,
            len(msgs), 
            10, 
            st, 
            '/messages/view/%s?page='%id
        ),
    ))

