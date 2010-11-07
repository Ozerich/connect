from django.db import models


class Faculty(models.Model):
    name = models.CharField('Name', max_length=200)
    community = models.ForeignKey('Community')

    def __unicode__(self):
        return self.name


class Stream(models.Model):
    name = models.CharField('Name', max_length=200)
    gid = models.CharField('Code', max_length=200)
    faculty = models.ForeignKey(Faculty)
    community = models.ForeignKey('Community')
    
    def __unicode__(self):
        return self.name


class Group(models.Model):
    name = models.CharField('Name', max_length=200)
    stream = models.ForeignKey(Stream)
    faculty = models.ForeignKey(Faculty)
    community = models.ForeignKey('Community')
    
    def __unicode__(self):
        return self.name


class Language(models.Model):
    name = models.CharField('Name', max_length=200)

    def __unicode__(self):
        return self.name
    
    
class Friendship(models.Model):
    src = models.ForeignKey('User', related_name='+')
    dst = models.ForeignKey('User', related_name='+')

    def __unicode__(self):
        return '%s > %s' % (self.src.__unicode__(), self.dst.__unicode__())
    
    
class User(models.Model):
    email = models.CharField('E-mail', max_length=200)
    password =  models.CharField('Password', max_length=200)
    number = models.CharField('Private number', max_length=7)
    name = models.CharField('First name', max_length=200)
    surname = models.CharField('Surname', max_length=200)
    birthday = models.DateField('Birthday')
    stream = models.ForeignKey(Stream)
    group = models.ForeignKey(Group)
    subgroup = models.IntegerField('Subgroup')
    language = models.ForeignKey(Language)
    
    friends = models.ManyToManyField('self', symmetrical=False, through=Friendship)
    communities = models.ManyToManyField('Community')
    
    avatar = models.CharField('Avatar file', max_length=200)

    def __unicode__(self):
        return '%s %s' % (self.name, self.surname)

    @property
    def full_name(self):
        return self.__unicode__()
    
class Message(models.Model):   
    src = models.ForeignKey(User, related_name='outbox')
    dst = models.ForeignKey(User, related_name='inbox')
    owner = models.ForeignKey(User, related_name='+')
    text = models.CharField('Text', max_length=2000)
    unread = models.IntegerField('Unread')
    date = models.DateTimeField('Sent on')
    attachments = models.ManyToManyField('File')
    
    def __unicode__(self):
        return self.text[:50]


class Community(models.Model):
    name = models.CharField('Name', max_length=200)
    parent = models.ForeignKey('Community', blank=True, null=True)
    rank = models.IntegerField('Rank')
    files = models.ManyToManyField('File', blank=True)
    
    def __unicode__(self):
        return self.name
    

class Topic(models.Model):    
    community = models.ForeignKey('Community')
    name = models.CharField('Name', max_length=200)
    date = models.DateTimeField('Last reply')
    root = models.ForeignKey('Comment', related_name='+',null=True)

    def __unicode__(self):
        return self.name


class Comment(models.Model):   
    author = models.ForeignKey('User')
    text = models.CharField('Text', max_length=2000)
    date = models.DateTimeField('Sent on')
    topic = models.ForeignKey('Topic')
    parent = models.ForeignKey('Comment', blank=True, null=True)
    attachments = models.ManyToManyField('File')

    def __unicode__(self):
        return self.text[:50]


class File(models.Model):   
    author = models.ForeignKey('User')
    name = models.CharField('Name', max_length=2000)
    date = models.DateTimeField('Uploaded')

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    short_name = models.CharField("Short name", max_length = 20)
    full_name = models.CharField("Full name", max_length = 100)
    community = models.ForeignKey("Community")
    
    def __unicode__(self):
        return self.short_name

class RatingType(models.Model):
    name = models.CharField("Name", max_length = 100)
    plus = models.CharField("Plus", max_length = 100)
    minus = models.CharField("Minus", max_length = 100)

    def __unicode__(self):
        return self.name
    
class Rating(models.Model):
    plus = models.IntegerField("Plus")
    minus = models.IntegerField("Minus")
    cls = models.ForeignKey("RatingType")
    
    def __unicode__(self):
        try:
            return '%s (%s)' % (self.cls.name, self.lector_set.all()[0].full_name)
        except:
            return self.cls.name
            
class Lector(models.Model):
    full_name = models.CharField("Full name", max_length = 100)
    subjects = models.ManyToManyField("Subject")
    photo = models.CharField("photo", max_length = 200)
    rating = models.ManyToManyField("Rating")
    
    def __unicode__(self):
        return self.full_name

class LectorComment(models.Model):   
    author = models.ForeignKey('User')
    text = models.CharField('Text', max_length=2000)
    date = models.DateTimeField('Sent on')
    
    lector = models.ForeignKey("Lector")   
       
    def __unicode__(self):
        return self.text[:50]

