from django.urls import path
from Landing import views

app_name = 'Landing'

urlpatterns = [
    path('', views.land, name='landing'),
]
