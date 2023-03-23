from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    icon_code = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_user')
    def get_absolute_url(self):
        return reverse('question_detail', args=([str(self.id)]))
    
    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField()
    date = models.DateField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User)
    dislikes = models.ManyToManyField(User, related_name='answer_dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('question_detail', args=([str(self.question.id)]))
    
    def __str__(self):
        return self.title


class Reply(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField()
    date = models.DateField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('answer_detail', args=([str(self.answer.id)]))
    
    def __str__(self):
        return self.title

class Badge(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='main_app/static/images/badges/', blank=True)
    point_limit = models.IntegerField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='main_app/static/images/profile/', blank=True)
    bio = models.TextField(max_length=250, blank=True)
    badges = models.ManyToManyField(Badge)

    def __str__(self):
        return str(self.user)