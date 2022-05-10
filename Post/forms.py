from django import forms
from . models import Posting


class PostForm(forms.ModelForm):

    class Meta:
        model = Posting
        fields = ['title', 'visualhearing', 'pic', 'body']

    title = forms.CharField()
    pic = forms.ImageField()
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
        )
    visualhearing = forms.ChoiceField(choices=((0, '시각'), (1, '청각')))
