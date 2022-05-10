
from django import forms
from . models import Qna_Posting


class PostForm(forms.ModelForm):
    class Meta:
        model = Qna_Posting
        fields = ['title', 'pic', 'body']
    title = forms.CharField()
    pic = forms.ImageField()
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
                }))
