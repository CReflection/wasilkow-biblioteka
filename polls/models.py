import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField('Pytanie', max_length=200)
    image = models.ImageField('Obrazek', null=True, blank=True, upload_to="images/")
    

    def __str__(self):
        return str(self.question_text)
    
    def get_answers(self):
        return self.answer_set.all()
    
    class Meta:
        verbose_name = "pytanie"
        verbose_name_plural = "Pytania"

class Answer(models.Model):
    answer_text = models.CharField('odpowiedź', max_length=200)
    valid = models.BooleanField('poprawna odpowiedź', default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.answer_text)
    
    class Meta:
        verbose_name = "odpowiedź"
        verbose_name_plural = "Odpowiedzi"

# Create your models here.