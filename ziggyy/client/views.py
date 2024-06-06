from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from client.forms import *
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def home(request):
    un=request.session.get('username')
    if un:
        client_object=User.object.get('username')
        d={'CO':client_object}
        return render(request,'home.html',d)
    return render(request,'home.html')


def client_registration(request):
    ECFO=ClientForm()
    d={'ECFO':ECFO}
    if request.method=='POST':
        CFDO=ClientForm(request.POST)
        if CFDO.is_valid():
            pw=CFDO.cleaned_data.get('password')
            MCFDO=CFDO.save(commit=False)
            MCFDO.set_password(pw)
            MCFDO.save()
        return HttpResponseRedirect(reverse('client_login'))
    return render(request,'client_registration.html',d)



def client_login(request):
    if request.method=='POST':
        un=request.POST.get('un')
        pw=request.POST.get('pw')
        ACO=authenticate(username=un,password=pw)
        if ACO and ACO.is_active:
            login(request,ACO)
            request.session['username']=un
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse('Invalid Credentials')
    return render(request,'client_login.html')

def client_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

