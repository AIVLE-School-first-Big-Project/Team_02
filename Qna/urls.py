from django.urls import path
from Qna import views


app_name = 'Qna'
urlpatterns = [
    path('', views.qna_post, name='qna_post'),
    path('form/', views.form, name='form'),
    path('<int:pk>/', views.qna_detail, name='qna_detail'),
    path('<int:pk>/edit/', views.qna_edit, name='qna_edit'),
    path('<int:pk>/delete/', views.delete, name='qna_delete'),
]
