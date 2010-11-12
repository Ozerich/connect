#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from datetime import *


def sendmsg(request, id):
    init(request)
    cu = request.user
    user = User.objects.get(id=id)
    m1 = Message(
        src=cu,
        dst=user,
        owner=cu,
        date=datetime.now(),
        text=request.POST['text'],
        unread=0
    )
    m2 = Message(
        src=cu,
        dst=user,
        owner=user,
        date=datetime.now(),
        text=request.POST['text'],
        unread=1
    )
    m1.save()
    m2.save()
    if 'attachment[]' in request.POST:
        for k in request.POST.getlist('attachment[]'):
            m1.attachments.add(File.objects.get(id=k))  
            m2.attachments.add(File.objects.get(id=k))
    m1.save()
    m2.save()
    return HttpResponseRedirect('/messages/view/%i'%user.id)


def deletemsg(request, id):
    init(request)
    cu = request.user
    try:
        m = Message.objects.get(owner=cu, id=id)
        user = m.src if m.src != cu else m.dst
        m.delete()
        return HttpResponseRedirect('/messages/view/%i'%user.id)
    except Message.DoesNotExist:
        pass
    return HttpResponseRedirect('/messages')


def messages(request):
    init(request)
    cu = request.user
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
    
    return HttpResponse(make_template(
        request, 
        'messages.html',
        senders=senders,
        title='Сообщения',
        current=2,
        notification=notify, 
    ))

