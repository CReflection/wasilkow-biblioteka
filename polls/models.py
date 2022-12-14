import datetime

from django.db import models
from django.utils import timezone
from datetime import timedelta

class Group(models.Model):
    name = models.CharField('Grupa', max_length=120)
    hash = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return str(self.name)
    
    def get_question(self):
        return self.question_set.all()

    class Meta:
        verbose_name_plural = "Grupy pytań"

class Question(models.Model):
    question_text = models.CharField('Pytanie', max_length=200)
    quote = models.CharField('Cytat', null=True, blank=True, max_length=300)
    image = models.ImageField('Obrazek', null=True, blank=True, upload_to="images/")
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    
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

class ScoreBoard(models.Model):
    name = models.CharField('Uczestnik',max_length=120)
    score = models.IntegerField('wynik')
    time_passed = models.DurationField(null=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = "uczestnik"
        verbose_name_plural = "Tablica wyników"


# Create your models here.