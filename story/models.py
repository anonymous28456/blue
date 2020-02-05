import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=20)

    
class Genre(models.Model):
    GENRES = (
        ('fiction', "短篇小說"),
        ('poety', "詩"),
        ('joke', "笑話"),
        ('illustration', "插畫"),
        ('rap', "饒舌"),
    )
    title = models.CharField(max_length=200, choices=GENRES)
    
    def __str__(self):
        return self.title


class Wish(models.Model):
    User = get_user_model()
    wisher = models.ForeignKey(User, models.SET_NULL,null=True, related_name='wish_made')
    genre = models.ManyToManyField(Genre)
#    title = models.CharField(max_length=20)
    content = models.CharField(max_length=1000)
    wish_time = models.DateTimeField(auto_now_add=True)
    heard_time = models.DateTimeField(null=True)
    finished_time = models.DateTimeField(null=True)
    sent_time = models.DateTimeField(null=True)
    
    User = get_user_model()
    granter = models.ForeignKey(User,models.SET_NULL,null=True, related_name='wish_fulfilled')
    price = models.IntegerField(null=False, blank=False)
    money_received = models.BooleanField(default=False)


    def __str__(self):
        return self.content



class Project(models.Model):
    User = get_user_model()
    creator = models.ForeignKey(User, models.CASCADE)
    title = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    pub_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='projects/{0}/{1}'.format(creator,title))
    content = models.CharField(max_length=1000, default="預設是無言")

    def __str__(self):
        return self.content


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - date.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
