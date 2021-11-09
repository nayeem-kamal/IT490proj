from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from API import API

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            
            print(name, email)
    form = ContactForm()
    return render(request, 'form.html', {'form': form})

def apiTest(request):
    rpc = API()
    print(" [x] Requesting current prices")
    response = rpc.getWeekBTC()
    print(" [.] Got %r" % response)
    form = ContactForm()
    return render(request, 'apiform.html', {'form': form})