from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
<<<<<<< HEAD
    path('qr/', views.qr, name='qr'),
=======
    path('question/', views.randomQuestion, name='randomQuestion'),
>>>>>>> f77b4deb88297bb92b88d35f60ff7c98e58a21d8
]