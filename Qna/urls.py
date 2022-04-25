from django.urls import path, include
from Qna import views


app_name = 'Qna'
urlpatterns = [
    path('', views.qna, name='qna'),
    path('Qedit/', views.qna_edit, name='qna_edit'),
    path('<int:pk>/', views.qna_detail, name = 'qna_detail'),

]
