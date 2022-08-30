from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),

    path('qr/', views.qr, name='qr'),
    path('question/', views.randomQuestion, name='randomQuestion'),
    path('wyniki/', views.score, name='wyniki'),
]
