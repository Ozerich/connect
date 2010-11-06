#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *


def community_tree(request):
    c = Community.objects.get(id=1)
    
    return main_template(
        request, 
        content=make_tree(c),
        title='Группы',
        current=4
    )

def make_tree(c):
    ch = ''.join(make_tree(cm) for cm in
        sorted(c.community_set.all(), key=lambda x:x.name))
    return make_template(
        'community-tree.html',
        community=c,
        children=ch
    )


def community_join(request, id):
    cu = current_user(request)
    try:
        cu.communities.add(Community.objects.get(id=id))
        cu.save()
        return HttpResponseRedirect('/community/'+id)
    except Community.DoesNotExist:
        raise Http404

        
def community_leave(request, id):
    cu = current_user(request)
    try:
        cu.communities.remove(Community.objects.get(id=id))
        cu.save()
        return HttpResponseRedirect('/community/'+id)
    except Community.DoesNotExist:
        raise Http404
        
        
def community(request, id):
    try:
        c = Community.objects.get(id=id)
    except Community.DoesNotExist:
        raise Http404
        
    topics = sorted(c.topic_set.all(), key=lambda x: x.date)
    topics = list(reversed(topics))
    
    subject = c.subject_set.all();
    if len(subject) != 0:
        subject = subject[0]
        lectors = subject.lector_set.all()
    else:  
        lectors = []
    try:
        st = int(request.GET['page'])*2-2
    except:
        st = 0
    
    content = make_template(
        'community.html',
        c=c,
        lectors=lectors,
        ismygroup=c in current_user(request).communities.all(),
        pager=make_paginator(len(topics), 2, st, '/community/%s?page='%id),
        topics=topics[st:st+2],
        files=c.files.all()[:5]
    )
    
    return main_template(
        request, 
        content=content,
        title=c.name,
        current=4
    )
