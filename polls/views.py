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
    if not request.session.get('answered_questions',None):
        request.session['answered_questions'] = ""
    
    print(request.session['answered_questions'])
    cookie_list = request.session['answered_questions'].split("'").pop()
    print(cookie_list)
    if str(question_id) in cookie_list:
        return HttpResponse("Już odpowiedziałeś :]")
    if request.method == "POST":
        request.session['answered_questions'] += str(question_id) + "'"
        print("grok", request.session.get('answered_questions',question_id))
        answer = get_object_or_404(Answer, pk=request.POST['answer'])
        if(answer.valid):
            return HttpResponse("'" + answer.answer_text + "' jest poprawną odpowiedzią na pytanie '" +question.question_text + "'")
        else:
            return HttpResponse("'" + answer.answer_text + "' nie jest poprawną odpowiedzią na pytanie '" +question.question_text + "'")

    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


