from django.urls import path, include
from Qna import views


app_name = 'Qna'
urlpatterns = [
    path('', views.index, name='index'),

]
