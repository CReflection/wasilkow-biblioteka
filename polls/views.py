import random

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render 

import qrcode
import qrcode.image.svg
from io import BytesIO

from .models import Question, Answer, ScoreBoard, Group


def index(request):
    latest_question_list = Question.objects.all()
    if not request.session.get('points', None):
        request.session['points'] = 0
    context = {
        'latest_question_list': latest_question_list,
        'points': request.session['points']
    }
    #print("Question ID(index) =", request.session['picked_question_id'])
    return render(request, 'polls/index.html', context)

#Sprawdzanie czy jesteś w trakcie odpowiadania na inne pytanie
#(jeżeli ktoś np zrefreshował stronę po otrzymaniu pytania)
def getRandomQuestionId(request, question_id_list):
    cookie_list = set(request.session['answered_questions'].split("'"))
    #Wybierz pytanie na które jeszcze użytownik nie odpowiedział za pomocą cookiesów i wszystkich pytań
    possible_ids = list(question_id_list - cookie_list)
    if possible_ids:
        question_id = int(random.choice(possible_ids))
        return question_id
    else:
        return None

def randomQuestion(request):
    if not request.session.get('points', None):
        request.session['points'] = 0
    if request.method == "POST":
        question_id = request.POST['question_id']
        question = get_object_or_404(Question, pk=question_id)
        answer = get_object_or_404(Answer, pk=request.POST['answer'])
        request.session['picked_question_id'] = None
        
        cookie_list = request.session['answered_questions'].split("'")
        if str(question_id) in cookie_list:
            return HttpResponse("Coś poszło nie tak, już odpowiedziałeś na to pytanie spróbuj ponownie.")

        request.session['answered_questions'] += str(question_id) + "'"
        if(answer.valid):
            request.session['points'] += 1
            latest_question_list = Question.objects.all()
            context = {
                'latest_question_list': latest_question_list,
                'points': request.session['points'],
                'alert': 'Odpowiedziałeś poprawnie na ten QR, znajdź następny :)',
            }
            return render(request, 'polls/index.html', context)
        else:
            list_of_ids = set(str(x) for x in Question.objects.all().values_list('id', flat=True))
            new_question_id = getRandomQuestionId(request,list_of_ids)
            if not new_question_id:
                return HttpResponse("Skończyły się już pytania :P")
            question = get_object_or_404(Question, pk=new_question_id)
            request.session['picked_question_id'] = new_question_id
            context = {
                'question': question,
            }
            return render(request, 'polls/detail.html', context)

    #Jeżeli nie odpowiedziałeś na żadne pytanie wcześniej ustaw zmienną w cookies
    #Która będzie trzymała te informacje
    if not request.session.get('answered_questions',None):
        request.session['answered_questions'] = ""
    
    if not request.session.get('picked_question_id', None):
        list_of_ids = set(str(x) for x in Question.objects.all().values_list('id', flat=True))
        question_id = getRandomQuestionId(request, list_of_ids)
    else:
        #Jeżeli w trakcie odpowiadania na pytanie przydziel odpowiednie pytanie
        question_id = int(request.session['picked_question_id'])
    if not question_id:
        return HttpResponse("Skończyły się już pytania :P")
    request.session['picked_question_id'] = str(question_id)
    question = get_object_or_404(Question, pk=question_id)
    print(request.session['picked_question_id'])
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)
    
def score(request):
    participants = ScoreBoard.objects.all().order_by('-score')
    return render(request, "polls/score_board.html", {'participants': participants})

def qr(request):
    context = {}
    if request.method == "POST":
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(request.POST.get("qr_text",""), image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()

    return render(request, "polls/generator_qr.html", context=context) 

def groupQuestion(request, group_hash):
    if not request.session.get('points', None):
        request.session['points'] = 0
    if not request.session.get('answered_groups', None):
        request.session['answered_groups'] = ""
    
    answered_groups = request.session['answered_groups'].split("'")
    print(answered_groups)
    if str(group_hash) in answered_groups:
        return HttpResponse("Już odpowiedziałeś na pytania w tym miejscu")
    group_question_ids = get_object_or_404(Group, hash=group_hash).question_set.all()
    group_question_ids = set(str(x) for x in group_question_ids.values_list('id', flat=True))

    if request.method == "POST":
        question_id = request.POST['question_id']
        question = get_object_or_404(Question, pk=question_id)
        answer = get_object_or_404(Answer, pk=request.POST['answer'])
        request.session['picked_question_id'] = None
        
        cookie_list = request.session['answered_questions'].split("'")
        if str(question_id) in cookie_list:
            request.session['answered_groups'] += str(group_hash) + "'"
            return HttpResponse("Coś poszło nie tak, już odpowiedziałeś na to pytanie spróbuj ponownie.")

        request.session['answered_questions'] += str(question_id) + "'"
        if(answer.valid):
            request.session['points'] += 1
            latest_question_list = Question.objects.all()
            context = {
                'latest_question_list': latest_question_list,
                'points': request.session['points'],
                'alert': 'Odpowiedziałeś poprawnie na ten QR, znajdź następny :)',
            }
            return render(request, 'polls/index.html', context)
        else:
            new_question_id = getRandomQuestionId(request,group_question_ids)
            if not new_question_id:
                request.session['answered_groups'] += str(group_hash) + "'"
                return HttpResponse("Skończyły się już pytania :P")
            question = get_object_or_404(Question, pk=new_question_id)
            request.session['picked_question_id'] = new_question_id
            context = {
                'question': question,
            }
            return render(request, 'polls/detail.html', context)

    #Jeżeli nie odpowiedziałeś na żadne pytanie wcześniej ustaw zmienną w cookies
    #Która będzie trzymała te informacje
    if not request.session.get('answered_questions',None):
        request.session['answered_questions'] = ""
    
    if not request.session.get('picked_question_id', None):
        question_id = getRandomQuestionId(request,group_question_ids)
    else:
        #Jeżeli w trakcie odpowiadania na pytanie przydziel odpowiednie pytanie
        question_id = int(request.session['picked_question_id'])
    if not question_id:
        return HttpResponse("Skończyły się już pytania :P")
    request.session['picked_question_id'] = str(question_id)
    question = get_object_or_404(Question, pk=question_id)
    print(request.session['picked_question_id'])
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)

def detail(request, question_id):
    if not request.session.get('points', None):
        request.session['points'] = 0
    question = get_object_or_404(Question, pk=question_id)
    if not request.session.get('answered_questions',None):
        request.session['answered_questions'] = ""

    cookie_list = request.session['answered_questions'].split("'").pop()
    if str(question_id) in cookie_list:
        return HttpResponse("Już odpowiedziałeś :]")
    if request.method == "POST":
        request.session['answered_questions'] += str(question_id) + "'"
        answer = get_object_or_404(Answer, pk=request.POST['answer'])
        if(answer.valid):
            request.session['points'] += 1
            return HttpResponse("'" + answer.answer_text + "' jest poprawną odpowiedzią na pytanie '" +question.question_text + "'")
        else:
            return HttpResponse("'" + answer.answer_text + "' nie jest poprawną odpowiedzią na pytanie '" +question.question_text + "'")
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)
