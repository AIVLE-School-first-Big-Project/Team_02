from django.urls import path, include
from Translation import views
app_name = 'Translation'


urlpatterns = [
        path('', views.index, name='index'),

]
