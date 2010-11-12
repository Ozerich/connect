#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from datetime import *

        
def topic(request, id):
    init(request)
    try:
        t = Topic.objects.get(id=id)
    except Topic.DoesNotExist:
        raise Http404
	
    if not t.root:
        c = Comment(
            text=t.name, 
            author=request.user,
            date=datetime.now(), 
            topic=t
        )
        c.save()
        t.root = c
        t.save()
 
    return HttpResponse(make_template(
        request, 
        'topic.html', 
        topic=t,
        comments=make_tree(request, t.root),
        title=t.name,
        current=4
    ))
    
    
def make_tree(r, c):
    ch = ''.join(make_tree(r, cm) for cm in
        sorted(c.comment_set.all(), key=lambda x:x.date))
    return make_template(
        r,
        'comment-tree.html',
        comment=c,
        children=ch
    )
    
    
def topic_reply(request):
    init(request)
    try:
        c = Comment.objects.get(id=request.POST['to'])
    except Comment.DoesNotExist:
        raise Http404
    
    c = Comment(
        text=request.POST['text'],
        author=request.user,
        parent=c,
        topic=c.topic,
        date=datetime.now(),
    )
    c.save()
     
    if 'attachment[]' in request.POST:
        for k in request.POST.getlist('attachment[]'):
            c.attachments.add(File.objects.get(id=k))  
    c.save()
    
    return HttpResponseRedirect('/topic/%i'%c.topic.id)
    
