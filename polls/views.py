from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render 

from .models import Question, Answer


def index(request):
    latest_question_list = Question.objects.all()
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=request.POST['answer'])
        if(answer.valid):
            return HttpResponse("Jest to poprawna odpowiedź na pytanie '" +answer.answer_text + "'")
        else:
            return HttpResponse("Nie jest to poprawna odpowiedź na pytanie '" +answer.answer_text + "'")

    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
