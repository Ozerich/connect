#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from datetime import *

        
def topic(request, id):
    try:
        t = Topic.objects.get(id=id)
    except Topic.DoesNotExist:
        raise Http404
    
    content = make_template(
        'topic.html',
        topic=t,
        comments=make_tree(t.root)
    )
    
    return main_template(
        request, 
        content=content,
        title=t.name,
        current=4
    )
    
    
def make_tree(c):
    ch = ''.join(make_tree(cm) for cm in
        sorted(c.comment_set.all(), key=lambda x:x.date))
    return make_template(
        'comment-tree.html',
        comment=c,
        children=ch
    )
    
    
def topic_reply(request):
    try:
        c = Comment.objects.get(id=request.POST['to'])
    except Comment.DoesNotExist:
        raise Http404
    
    Comment(
        text=request.POST['text'],
        author=current_user(request),
        parent=c,
        topic=c.topic,
        date=datetime.now(),
    ).save()
    
    return HttpResponseRedirect('/topic/%i'%c.topic.id)
    
