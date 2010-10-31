#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from datetime import *


def sendmsg(request, id):
    cu = current_user(request)
    user = User.objects.get(id=id)
    Message(
        src=cu,
        dst=user,
        owner=cu,
        date=datetime.now(),
        text=request.POST['text'],
        unread=0
    ).save()
    Message(
        src=cu,
        dst=user,
        owner=user,
        date=datetime.now(),
        text=request.POST['text'],
        unread=1
    ).save()
    return HttpResponseRedirect('/messages/view/%i'%user.id)


def deletemsg(request, id):
    cu = current_user(request)
    try:
        m = Message.objects.get(owner=cu, id=id)
        user = m.src if m.src != cu else m.dst
        m.delete()
        return HttpResponseRedirect('/messages/view/%i'%user.id)
    except Message.DoesNotExist:
        pass
    return HttpResponseRedirect('/messages')


def messages(request):
    cu = current_user(request)
    notify = None
    senders = []

    for msg in Message.objects.filter(owner=cu):
        if msg.dst != cu:
            m = msg.dst
        if msg.src != cu:
            m = msg.src
        if not m in senders:
            senders.append(m)
            m.msg_date = msg.date
            m.msg_count = 1
            m.msg_unread = msg.unread==1
        else:
            m = senders[senders.index(m)]
            m.msg_date = max(m.msg_date, msg.date)
            m.msg_count += 1
            m.msg_unread = m.msg_unread or (msg.unread==1)
        if m.msg_date == msg.date:
            m.msg_subj = msg.text[:40]
            
    if cu in senders:
        senders.remove(cu)        
            
    senders = sorted(senders, key=lambda f: f.msg_date)
    senders = reversed(senders)
    
    content = make_template(
        'messages.html',
        senders=senders,
    )
    return main_template(
        request, 
        content, 
        notification=notify, 
        title='Сообщения',
        current=2
    )
    
