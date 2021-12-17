from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from . import API
from . import DB
from .loginForm import loginForm
from .trade import tradeForm
import json
import ast
import datetime

email = ""
def contact(request):
    fname = []
    lname = []
    email = []
    passwd = []

    if request.method == 'POST':
        print("contactTestPost")
        form = ContactForm(request.POST)

        if form.is_valid():
            signup = DB.DB()
            fname = form.cleaned_data['firstName']
            lname = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['password']
            signup.register(email, fname, lname, passwd)

            print(fname, email, passwd, email, lname)
        form = ContactForm()
        return render(request, 'testRegistration.html', {'form': form, 'fname': fname, 'lname': lname, 'email': email, 'passwd': passwd})
    else:
        print("contactTestGet")
        form = ContactForm(request.GET)

        if form.is_valid():
            signup = DB.DB()
            fname = form.cleaned_data['firstName']
            lname = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['password']
            signup.register(email, fname, lname, passwd)

            print(fname, email, passwd, email, lname)
        form = ContactForm()
        return render(request, 'testRegistration.html', {'form': form, 'fname': fname, 'lname': lname, 'email': email, 'passwd': passwd})


def apiTest(request):
    rpc = API.API()

    print(" [x] Requesting current prices")
    rawResponse = json.dumps(rpc.getWeekBTC().decode("UTF-8"))
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
    # return render(request, 'charts.html', {'form': form,'response':response, 'currentPrice':currentPrice})
    return render(request, 'charts.html', {'form': form, 'rKeys': rKeys, 'rVals': rVals})


def login(request):
    global email
    em = []
    passwd = []
    login = DB.DB()
    print("test")

    if request.method == 'POST':
        email = ""
        form = loginForm(request.POST)
        print("testpost")
        print(request.POST)
        if form.is_valid():

            em = form.cleaned_data['email']
            email = em
            passwd = form.cleaned_data['password']
            # login.login(email,passwd)
            rawLogin = json.dumps(login.login(em, passwd).decode("UTF-8"))
            print(em, passwd, email)
        form = loginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = loginForm(request.GET)
        print("testget")
        if form.is_valid():
            email = ""
            print("testif")

            em = form.cleaned_data['email']
            email = em
            passwd = form.cleaned_data['password']
            login.login(email, passwd)

            print(em, passwd,email)
            form = loginForm()
            return render(request, 'accounts.html', {'form': form})
        else:
            print("this returned false")
        return render(request, 'login.html', {'form': form})


def trade(request):
    print(email)
    source = []
    destination = []
    amount = []
    form = tradeForm(request.POST) 
    print(dict(form.data))
    
    if request.method == 'POST':
        #form = tradeForm(request.POST)
        if form.is_valid():
            formdict = dict(form.data)
            print(True)
            trade = DB.DB()
            source = formdict['source'][0]
            destination = formdict['destination'][0]
            amount = formdict['amount'][0]
            pub = form.cleaned_data['pub']
            trade.trade(source,destination,amount,email)
        else:
            print(False)
        
    return render(request, 'trade.html',{'form':form})


def accounts(request):
    global email
    dbAcc = DB.DB()
    getAcct = eval(json.loads(json.dumps(dbAcc.getAccounts(email).decode("UTF-8"))))
    aKeys = ["USD", "BTC", "ETH"]
    aValues = []
    aList = []
    i = 0
    for values in getAcct.values():
        #aValues.append(values[2])
        aList.append({aKeys[i]:values[2]})
        #aValues.append(values[2])
        print(aValues)
        i+=1
        #aList.append(dict(zip(aKeys,aValues)))
        
    #getAcct = b"{'BTC': (31, 'newuser@gmail.com', 0.0, 'BTC'), 'ETH': (32, 'newuser@gmail.com', 0.0, 'ETH'), 'USD': (30, 'newuser@gmail.com', 10000.0, 'USD')}"
    print(getAcct)
    return render(request, 'accounts.html', {'getAcct': aList, 'aKeys':aKeys})


def history(request):
    
    getHist = DB.DB()

    # histRaw = b"{'BTC': (31, 'newuser@gmail.com', 0.0, 'BTC'),
    #  'ETH': (32, 'newuser@gmail.com', 0.0, 'ETH'), 'USD': (30, 'newuser@gmail.com', 10000.0, 'USD')}"
    histRaw = eval(
        (json.loads(json.dumps(getHist.tradeHistory(email).decode("UTF-8")))))
    #histRaw = json.dumps(getHist.tradeHistory(email).decode("UTF-8"))

    map = {}
    acc = ast.literal_eval(json.loads(json.dumps(getHist.getAccounts(email).decode("UTF-8"))))
    #acc = {'BTC': (31, 'newuser@gmail.com', 100.0, 'BTC'), 'ETH': (32, 'newuser@gmail.com', -
      #                                                             100.0, 'ETH'), 'USD': (30, 'newuser@gmail.com', 10000.0, 'USD')}
    for i in acc.keys():
        map[i] = acc[i][0]
    newHist = ()
    inv_map = {v: k for k, v in map.items()}

            
    hkeys = ("tID", "src", "dst", "amt", "created")
    hlist = []

    for values in histRaw:
        hlist.append(dict(zip(hkeys,values)))
    print(hlist)
    print(type(histRaw))

    #getHist = histRaw
    print(hlist)
    print(inv_map)

    historyKeys = []

    return render(request, 'history.html', {'getHist': hlist, "tradehistory": histRaw, 'map': inv_map})


def ledger(request):
    rpc = API.API()
    ledgeData = json.loads(rpc.getLedger().decode("utf-8"))["Data"]
    return render(request, 'ledger.html', {"ledgeData": ledgeData})

def learn(request):
    return render(request, 'learn.html')
