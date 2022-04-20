from django.urls import path
from Post import views

app_name = 'Post'


urlpatterns = [
    path('', views.post, name='post'),
    path('edit/', views.edit, name='edit'),
]