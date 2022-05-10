from django.urls import path
from Translation import views
app_name = 'Translation'


urlpatterns = [
        path('', views.home, name='index'),
        path('signlanguage/', views.signlanguage, name='signlanguage'),
        path('braille/', views.braille, name='braille'),
        path('textlanguage/', views.textlanguage, name='textlanguage'),
        path('soundlanguage/', views.soundlanguage, name='soundlanguage'),
        path('textlanguage2/', views.textlanguage2, name='textlanguage2'),
        path('textlanguage2_trans/', views.textlanguage2_trans,
             name='textlanguage2_trans'),
]
