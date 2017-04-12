from django import forms

from .models import Test

class PostForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('name', 'desc','requirement','stepdesc','stepexpresult')