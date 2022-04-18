from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=150, label="아이디", error_messages={'unique':"이미 존재하는 아이디입니다."})
    name = forms.CharField(max_length=128, label="이름")
    email = forms.EmailField(max_length=128, label="이메일", error_messages={'unique':"이미 존재하는 이메일입니다."})
    class Meta:
            model = User
            fields = ("username", 'name', 'email', "password1", "password2" )
            

class LoginForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            "username": "아이디",
        }
 
    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("로그인 실패")
        
class UpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['name'].disabled = True
    class Meta:
        model = User
        fields = ("username", 'name', 'email', )
        labels = {
            "username": "아이디",
            "name" : "이름",
            "email" : "이메일",
        }
        
class PasswordVerificationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            "username": "아이디",
            "password" : "비밀번호"
        }
 
    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("비밀번호가 일치하지 않습니다.")  
            
class ParamForm(forms.Form):
    username = forms.CharField(label='아이디')
    email = forms.CharField(label='이메일')
    
