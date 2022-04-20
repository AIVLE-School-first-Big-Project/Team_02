import email
from genericpath import exists
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from requests import session
from .models import User
# from Post.models import Posting
from .forms import SignupForm, LoginForm, UpdateForm, PasswordVerificationForm, ParamForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode


def if_session(request):
     username = request.session.get('username')
     if username:
          user = User.objects.get(username = username)
          return user.username
          
def signup(request):
     context = {}
     if request.method == 'POST':
          form = SignupForm(request.POST)
          if form.is_valid():
               form.save()
               username = form.cleaned_data.get('username')
               name = form.cleaned_data.get('name')
               email = form.cleaned_data.get('email')
               raw_password = form.cleaned_data.get('password1')
               
               user = authenticate(username=username, password=raw_password)
               # login(request, user)
               return redirect('/user/login')
          else:
               context['signup_form'] = form
     else:
          form = SignupForm()
          context['signup_form'] = form
     return render(request, 'User/signup.html', context)

def login(request):
    context = {}
 
    user = request.user
    if user.is_authenticated:
        return redirect("/main")
 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                request.session['username'] = username
                return redirect("/main")
    else:
        form = LoginForm()
 
    context['login_form'] = form
 
    return render(request, "User/login.html", context)

def logout(request):
     auth_logout(request)
     return redirect('/main')

def delete(request, username):
     context = {}
     if request.method == 'POST':
          form = PasswordVerificationForm(request.POST, instance=request.user)
          if form.is_valid():
               password = request.POST.get('password')
               user = authenticate(username=username, password=password)
               if user:
                    user.delete()
                    logout(request)
                    return redirect('/main')
          else:
               context['error'] = '회원정보가 일치하지 않습니다.'
               render(request, "User/delete.html", context) 
     else:
          form = PasswordVerificationForm(instance=request.user)
     context['password_form'] = form
     return render(request, "User/delete.html", context)

def update(request, username):
     context = {}
     if request.method == 'POST':
          form = UpdateForm(request.POST, instance=request.user)
          form2 = PasswordChangeForm(request.user, request.POST)
          if form.is_valid() and form2.is_valid():
               form.save()
               user2 = form2.save()
               update_session_auth_hash(request, user2)
               logout(request)
               return redirect('/user/login')
     else:
          form = UpdateForm(instance=request.user)
          form2 = PasswordChangeForm(request.user)
     context['update_form'] = form
     context['pwupdate_form'] = form2
     return render(request, 'User/update.html', context)

def find_id(request):
     return render(request, 'User/find_id.html')

def show_id(request):
     confirm_email = request.GET.get('confirm_email')
     confirm_id = User.objects.get(email=confirm_email).username
     context = {'confirm_id' : confirm_id}
     return JsonResponse(context)

def mypage(request, username):
     user = User.objects.get(username=username)
     context = {}
     # posts = Posting.objects.filter(id = userindex).values().order_by('-date')
     # if len(posts) >= 5:
     #      posts = posts[0:5]
     # context['posts'] = posts
     if user:
          context['username'] = user
          return render(request, 'user/mypage.html', context)
     else:
          return redirect('/main')

def active_message(username_64):
     LENGTH = 8
     string_pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*'
     newpassword = ""
    
     for _ in range(LENGTH):
          newpassword += random.choice(string_pool)
          
     user = User.objects.get(username=force_text(urlsafe_base64_decode(username_64)))
     user.password = make_password(newpassword)
     user.save()
     return f"비밀번호 재발급\n\n 비밀번호 : {newpassword}\n\n감사합니다."

def find_pw(request):
     context = {}
     if request.method == 'POST':
          form = ParamForm(request.POST)
          try:
               username = request.POST.get('username')
               email = request.POST.get('email')
               confirm_username = User.objects.get(email=email).username
               confirm_email = User.objects.get(username=username).email
               if confirm_email == email and confirm_username == username:
                    user = User.objects.get(username=username)
                    username_64 = urlsafe_base64_encode(force_bytes(username))
                    message_data = active_message(username_64)
                    mail_title = "비밀번호 재발급"
                    mail_to = user.email
                    email = EmailMessage(mail_title, message_data, to=[mail_to])
                    email.send()
                    return redirect('/user/login')
               context['error'] = '일치하는 정보가 없습니다.'
          except ObjectDoesNotExist:
               context['error'] = '일치하는 정보가 없습니다.'
     else:
          form = ParamForm()
     context['param_form'] = form
     return render(request, "User/find_pw.html", context)


def test(request):
     return render(request, "../templates/base.html")
