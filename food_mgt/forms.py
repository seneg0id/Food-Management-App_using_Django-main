from dataclasses import fields
from django import forms
from .models import Post

class statusupdate(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['status']

