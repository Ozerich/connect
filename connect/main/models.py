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


class Community(models.Model):
    name = models.CharField('Name', max_length=200)
    parent = models.ForeignKey('Community', blank=True, null=True)
    rank = models.IntegerField('Rank')

    def __unicode__(self):
        return self.name
    
