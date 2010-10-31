#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from datetime import *


def viewmsg(request, id):
    cu = current_user(request)
    notify = None
    senders = []
    
    user = User.objects.get(id=id)
    msgs = []
    msgs.extend(Message.objects.filter(src=user, owner=cu))
    msgs.extend(Message.objects.filter(dst=user, owner=cu))
    msgs = sorted(msgs, key=lambda x: x.date)
    msgs = [m for m in reversed(msgs)]
    
    if 'ajax' in request.GET:
        st = int(request.GET['ajax'])
        msgs = msgs[st:st+10]
    else:
        msgs = msgs[:10]
    
    content = make_template(
        'messages-view.html',
        u=user,
        messages=msgs,
        me=cu,
        ajax=('ajax' in request.GET)
    )

    if 'ajax' in request.GET:
        return HttpResponse(content)
    
    for m in msgs:
        if m.unread == 1:
            m.unread = 0
            m.save()
                    
    return main_template(
        request, 
        content, 
        title='Сообщения',
        current=2
    )

