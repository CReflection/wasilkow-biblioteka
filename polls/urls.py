from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),

    path('<int:question_id>/', views.detail, name='detail'),
    path('question/', views.randomQuestion, name='randomQuestion'),
    path('quiz/<slug:group_hash>', views.groupQuestion, name='groupQuestion'),
    
    path('qr/', views.qr, name='qr'),
    
    path('wyniki/', views.score, name='wyniki'),
]
