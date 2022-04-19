
from attr import attrs
from django import forms
from django.forms import TextInput, Textarea
from . models import Posting


class PostForm(forms.ModelForm):
    class Meta:
        model = Posting
        fields = ['title','visualhearing' , 'pic', 'body']
    title = forms.CharField()
    pic = forms.ImageField()
    body = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}))
    visualhearing = forms.ChoiceField(choices = ((0,'시각'),(1,'청각')))
    #title.widget.attrs.update({'class':'form-control'})

    