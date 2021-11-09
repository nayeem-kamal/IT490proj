from django import forms

class ContactForm(forms.Form):
    firstName = forms.CharField(label='First Name')
    lastName = forms.CharField(label='Last Name')
    email = forms.EmailField(label='E-Mail')
    password = forms.CharField(widget=forms.PasswordInput)

