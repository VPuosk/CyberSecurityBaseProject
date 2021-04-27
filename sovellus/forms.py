from django import forms

class PostForm(forms.Form):
    header = forms.CharField(label='Header')
    text = forms.CharField(label='Text')

class FilterForm(forms.Form):
    text = forms.CharField(label="Filter")