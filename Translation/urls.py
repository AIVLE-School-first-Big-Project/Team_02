from django.urls import path, include
from Translation import views
app_name = 'Translation'


urlpatterns = [
        path('', views.home, name='index'),
        path('signlanguage/', views.signlanguage, name='signlanguage'),
        path('braille/', views.braille, name='braille'),
        path('textlanguage/', views.textlanguage, name='textlanguage'),
        path('soundlanguage/', views.soundlanguage, name='soundlanguage'),
        path('model/', views.sts_model, name='model'),
]
