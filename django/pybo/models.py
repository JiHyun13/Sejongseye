from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 모델 변경시 >>> python manage.py makemigrations >>> python manage.py migrate

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True ,blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateField()
    modify_date = models.DateTimeField(null=True ,blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')