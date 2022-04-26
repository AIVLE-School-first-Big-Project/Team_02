from django.urls import path
from Post import views

app_name = 'Post'


urlpatterns = [
    path('', views.show, name='show'),
    path('form/', views.form, name = 'form'),
    path('<int:pk>/', views.detail, name = 'detail'),
    path('<int:pk>/edit/' , views.edit , name = 'edit'),
    path('<int:pk>/delete/' , views.delete , name = 'delete'),
]