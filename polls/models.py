import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    #created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question_text)
    
    def get_answers(self):
        return self.answer_set.all()
    
    class Meta:
        verbose_name_plural = "Pytania"

class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    valid = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.answer_text)
    
    class Meta:
        verbose_name_plural = "Odpowiedzi"

# Create your models here.