#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from datetime import *


def community_tree(request):
    init(request)
    c = Community.objects.get(id=1)
    
    return HttpResponse(make_template(
        request,
        'main.html',
        content=make_tree(request, c),
        title='Группы',
        current=4
    ))

def make_tree(req, c):
    ch = ''.join(make_tree(req, cm) for cm in
        sorted(c.community_set.all(), key=lambda x:x.name))
    return make_template(
        req,
        'community-tree.html',
        community=c,
        children=ch
    )


def community_join(request, id):
    init(request)
    cu = current_user(request)
    try:
        cu.communities.add(Community.objects.get(id=id))
        cu.save()
        return HttpResponseRedirect('/community/'+id)
    except Community.DoesNotExist:
        raise Http404

        
def community_leave(request, id):
    init(request)
    cu = current_user(request)
    try:
        cu.communities.remove(Community.objects.get(id=id))
        cu.save()
        return HttpResponseRedirect('/community/'+id)
    except Community.DoesNotExist:
        raise Http404
     
def community_addtopic(request, id):
    init(request)
    
    topic = Topic(
        community = Community.objects.get(id=id),
        name = request.POST['header'],
        date = datetime.now(),
        root = Comment()
    )
    topic.save()

    first_comment = Comment(
        author = request.user,
        date = datetime.now(),
        text = request.POST['text'],
        topic = topic
    )
    first_comment.save()
    
    topic.root = first_comment
    topic.save()
    
    return HttpResponseRedirect("/topic/"+str(topic.id))
    

def community_addfile(request, id):
    init(request)
    return HttpResponseRedirect("/community/"+id)
    
        
def community(request, id):
    init(request)
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
        st = int(request.GET['page'])*5-5
    except:
        st = 0
    
    return HttpResponse(make_template(
        request,
        'community.html',
        c=c,
        lectors=lectors,
        my_files = request.user.file_set.all(),
        ismygroup=c in request.user.communities.all(),
        pager=make_paginator(request, len(topics), 5, st, '/community/%s?page='%id),
        topics=topics[st:st+5],
        files=c.files.all()[:5],
        title=c.name,
        current=4
    ))
    
