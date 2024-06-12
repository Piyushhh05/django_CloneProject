from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from master.forms import *
from django.contrib.auth import authenticate,login
from django.urls import reverse
# Create your views here.
def home(request):
    return render(request,'home.html')


def master_registration(request):
    EMFO=MasterForm()
    d={'EMFO':EMFO}
    if request.method=='POST':
        MFDO=MasterForm(request.POST)
        if MFDO.is_valid():
            pw=MFDO.cleaned_data.get('password')
            MMFDO=MFDO.save(commit=False)
            MMFDO.set_password(pw)
            MMFDO.is_staff=True
            MMFDO.save()
            return HttpResponseRedirect(reverse('master_login'))
            
        return HttpResponse('Invalid Data')
    return render(request,'master_registration.html',d)


def master_login(request):
    if request.method=='POST':
        un=request.POST.get('un')
        pw=request.POST.get('pw')
        AMO=authenticate(username=un,password=pw)
        if AMO and AMO.is_active and AMO.is_staff:
            login(request,AMO)
            request.session['username']=un
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse('Invalid Credentials')
    return render(request,'master_login.html')


def master_items(request):
    EIFO=ItemForm()
    d={'EIFO':EIFO}
    if request.method=='POST' and request.FILES:
        IFDO=ItemForm(request.POST,request.FILES)
        if IFDO.is_valid():
            IFDO.save()
            return HttpResponse('Item Add Successfull')
        return HttpResponse('Invalid data')
    return render(request,'master_items.html',d)



def menu(request):
    items = Items.objects.all()
    d = {'items':items}
    return render(request,'menu.html', d)


def delete_item(request,pk):
    get_menu=Items.objects.get(items_id=pk)
    get_menu.delete()
    return HttpResponseRedirect(reverse('menu'))

    
def update_item(request,pk):
    get_menu=Items.objects.get(items_id=pk)
    get_menu.save()
    return HttpResponseRedirect(reverse('home'))