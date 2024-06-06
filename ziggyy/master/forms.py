from django import forms
from master.models import *
from django.contrib.auth.models import User

class MasterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']
        help_texts={'username':''}
        widgets={'password':forms.PasswordInput}

class ItemForm(forms.ModelForm):
    class Meta:
        model=Items
        fields='__all__'
        exclude=['items_id']
        