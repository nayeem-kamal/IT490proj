from django import forms

class loginForm(forms.Form):

    email = forms.EmailField(label='E-Mail')
    password = forms.CharField(widget=forms.PasswordInput)
    