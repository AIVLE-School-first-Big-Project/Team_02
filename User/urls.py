from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/<str:username>', views.delete, name='delete'),
    path('mypage/<str:username>', views.mypage, name='mypage'),
    path('find_id/', views.find_id, name='find_id'),
    path('find_id/show_id/', views.show_id, name='show_id'),
    path('find_pw/', views.find_pw, name='find_pw'),
    path('update/<str:username>', views.update, name='update'),
]