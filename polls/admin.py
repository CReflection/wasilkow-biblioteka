from django.contrib import admin
from .models import Question, Answer, ScoreBoard, Group

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class QuestInline(admin.StackedInline):
    model = Question
    fields = [ "question_text" ]
    readonly_fields = ['question_text',]

class GroupAdmin(admin.ModelAdmin):
    inlines = [QuestInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(ScoreBoard)
admin.site.register(Group, GroupAdmin)
# Register your models here.
