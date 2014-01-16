__author__ = 'DarkSector'
from django import forms
from models import Demo

class DemoForm(forms.ModelForm):
    class Meta():
        model = Demo

    def __init__(self, *args, **kwargs):
        super(DemoForm, self).__init__(*args, **kwargs)