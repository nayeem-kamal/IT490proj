from django import forms

class tradeForm(forms.Form):
    source = forms.CharField(label='Source')
    destination = forms.CharField(label='Destination')
    amount = forms.CharField(label='Amount')
    pub = forms.BooleanField(label="Make my trade public",required=False,widget=forms.widgets.CheckboxInput(attrs={'class': 'checkbox-inline'}))
    