from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from . import API
from . import DB
from .loginForm import loginForm
import json
def contact(request):
    fname = []
    lname = []
    email = []
    passwd = []

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            signup = DB.DB()
            fname = form.cleaned_data['firstName']
            lname = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['password']
            signup.register(email,fname,lname,passwd)

            print(fname, email, passwd,email,lname)
        form = ContactForm()
        return render(request, 'testRegistration.html', {'form': form, 'fname': fname, 'lname': lname, 'email': email, 'passwd': passwd})
    else:
        form = ContactForm(request.GET)

        if form.is_valid():
            signup = DB.DB()
            fname = form.cleaned_data['firstName']
            lname = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['password']
            signup.register(email,fname,lname,passwd)

            print(fname, email, passwd,email,lname)
        form = ContactForm()
        return render(request, 'testRegistration.html', {'form': form, 'fname': fname, 'lname': lname, 'email': email, 'passwd': passwd})
def apiTest(request):
    rpc = API.API()
 
    print(" [x] Requesting current prices")
    rawResponse =json.dumps(rpc.getWeekBTC().decode("UTF-8"))
    response = eval(json.loads(rawResponse))
    #response = dict(rawResponse)
    #currentPrice = rpc.getCurrentPrices()
    #response = {'2021-11-08 16:00:00': '68514.26', '2021-11-07 16:00:00': '67755.46', '2021-11-06 17:00:00': '63309.57', '2021-11-05 17:00:00': '61594.16', '2021-11-04 17:00:00': '62621.97', '2021-11-03 17:00:00': '63102.86', '2021-11-02 17:00:00': '63553.52'}
    print(response)
   
    
    rKeys = ""
    rVals = ""
    
    

    for keys in response.keys():
	    rKeys += keys + ", "
    for values in response.values():
	    rVals += values + ", "

    form = ContactForm()
    #return render(request, 'charts.html', {'form': form,'response':response, 'currentPrice':currentPrice})
    return render(request, 'charts.html', {'form': form,'rKeys':rKeys, 'rVals':rVals})

def login(request):


    email = []
    passwd = []

    if request.method == 'POST':
        form = loginForm(request.POST)

        if form.is_valid():
            login = DB.DB()

            email = form.cleaned_data['email']
            passwd = form.cleaned_data['password']
            login.login(email,passwd)

            print(email, passwd,)
        form = loginForm()
        return render(request,'login.html',{'form':form})
    else:
        form = loginForm(request.GET)

        if form.is_valid():
            login = DB.DB()

            email = form.cleaned_data['email']
            passwd = form.cleaned_data['password']
            login.login(email,passwd)

            print(email, passwd,)
        form = loginForm()
        return render(request,'login.html',{'form':form})  

def trade(request):

    return render(request,'trade.html')

def accounts(request):

    return render(request,'accounts.html')

def learn(request):

    return render(request,'learn.html')

def register(request):

    return render(request,'register.html')

def payment_deposit(request):

    return render(request,'payment_deposit.html')





