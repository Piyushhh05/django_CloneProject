from django import forms
from client.models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']
        help_texts={'username':''}
        widgets={'password':forms.PasswordInput}

