from django import forms

from .models import Load

class LoadForm(forms.ModelForm):
    class Meta:
        model = Load
        fields = ('title', 'file')
