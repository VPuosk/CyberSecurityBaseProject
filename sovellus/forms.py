from django import forms

class PostForm(forms.Form):
    header = forms.CharField(label='Header')
    text = forms.CharField(label='Text')