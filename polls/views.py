import random

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

#Sprawdzanie czy jesteś w trakcie odpowiadania na inne pytanie
#(jeżeli ktoś np zrefreshował stronę po otrzymaniu pytania)
def getRandomQuestionId(request):
    list_of_ids = set(str(x) for x in Question.objects.all().values_list('id', flat=True))
    cookie_list = set(request.session['answered_questions'].split("'"))
    #Wybierz pytanie na które jeszcze użytownik nie odpowiedział za pomocą cookiesów i wszystkich pytań
    possible_ids = list(list_of_ids - cookie_list)
    question_id = int(random.choice(possible_ids))
    return question_id

def randomQuestion(request):
    if request.method == "POST":
        question_id = request.session['picked_question_id']
        question = get_object_or_404(Question, pk=question_id)
        answer = get_object_or_404(Answer, pk=request.POST['answer'])
        request.session['picked_question_id'] = None
        
        cookie_list = request.session['answered_questions'].split("'").pop()
        if str(question_id) in cookie_list:
            return HttpResponse("Coś poszło nie tak, już odpowiedziałeś na to pytanie spróbuj ponownie.")

        request.session['answered_questions'] += str(question_id) + "'"
        if(answer.valid):
            return HttpResponse("'" + answer.answer_text + "' jest poprawną odpowiedzią na pytanie '" +question.question_text + "'")
        else:
            question = get_object_or_404(Question, pk=getRandomQuestionId(request))
            return render(request, 'polls/detail.html', {'question': question})

    #Jeżeli nie odpowiedziałeś na żadne pytanie wcześniej ustaw zmienną w cookies
    #Która będzie trzymała te informacje
    if not request.session.get('answered_questions',None):
        request.session['answered_questions'] = ""
    
    if not request.session.get('picked_question_id', None):
        question_id = getRandomQuestionId(request)
    else:
        #Jeżeli w trakcie odpowiadania na pytanie przydziel odpowiednie pytanie
        question_id = request.session['picked_question_id']
    request.session['picked_question_id'] = question_id
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    




