#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from datetime import *
from settings import *

def community_tree(request):
    if not init(request):
        return HttpResponseRedirect('/login')
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
        children=ch,
        is_link=c.id not in HIDDEN_COMMUNITY_NODES
    )


def community_join(request, id):
    if not init(request):
        return HttpResponseRedirect('/login')
    cu = request.user
    try:
        cu.communities.add(Community.objects.get(id=id))
        cu.save()
        return HttpResponseRedirect('/community/'+id)
    except Community.DoesNotExist:
        raise Http404

        
def community_leave(request, id):
    if not init(request):
        return HttpResponseRedirect('/login')
    try:
        request.user.communities.remove(Community.objects.get(id=id))
        request.user.save()
        return HttpResponseRedirect('/community/'+id)
    except Community.DoesNotExist:
        raise Http404
     
def community_addtopic(request, id):
    if not init(request):
        return HttpResponseRedirect('/login')
    
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
    
    NewsTopic.newtopic(request.user, topic)
    
    return HttpResponseRedirect("/topic/"+str(topic.id))

def community_addevent(request, id):
    if not init(request):
        return HttpResponseRedirect('/login')
    event = Event()
    event.community = Community.objects.get(id=id)
    event.name = request.POST['event_name']
    event.date_added = datetime.now()
    event.user_added = request.user
    
    date = request.POST['date'].split('/');
    event.date = datetime(int(date[2]), int(date[0]), int(date[1]))
    event.save()

    return HttpResponseRedirect("/community/"+str(id))

    
   
def community_addfile(request, c_id, f_id):

    file = File.objects.get(id=f_id)
    community = Community.objects.get(id=c_id)
    
    community.files.add(file)
    community.save()
    
    return HttpResponseRedirect('/community/' + str(c_id))
    
        
def community(request, id):
    if not init(request):
        return HttpResponseRedirect('/login')
    try:
        c = Community.objects.get(id=id)
    except Community.DoesNotExist:
        raise Http404
    
    try:
        admins = CommunityAdmin.objects.filter(user=request.user,community=c)
        admin = len(admins) > 0
    except Community.DoesNotExist:
        admin = False
           
    topics = sorted(c.topic_set.all(), key=lambda x: x.date)
    topics = list(reversed(topics))
    
    subject = c.subject_set.all();
    if len(subject) != 0:
        subject = subject[0]
        lectors = subject.lector_set.all()
    else:  
        lectors = []
    
    events = my_events(request, community=c)
    
    try:
        st = int(request.GET['page'])*5-5
    except:
        st = 0
    
    return HttpResponse(make_template(
        request,
        'community.html',
        c=c,
        admin=admin,
        events=events,
        lectors=lectors,
        my_files = request.user.file_set.all(),
        ismygroup=c in request.user.communities.all(),
        pager=make_paginator(request, len(topics), 5, st, '/community/%s?page='%id),
        topics=topics[st:st+5],
        files=c.files.all()[:5],
        title=c.name,
        current=4
    ))
    
