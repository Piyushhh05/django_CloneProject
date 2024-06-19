from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from master.forms import *
from django.contrib.auth import authenticate,login
from django.urls import reverse
from random import randint
from django.core.mail import send_mail
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


def changepassword(request):
    if request.method == 'POST':
        pw=request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            otp= randint(100000,999999)
            request.session['pw']=pw
            request.session['otp']=otp
            un=request.session.get('username')
            UO=User.objects.get(username=un)
            email=UO.email
            send_mail(
                "RE:- OTP for change the Password",
                f"OTP for change the Password is: {otp} ",
                'piyushgamechanger5@gmail.com',
                [email],
                fail_silently=False
            )
            return render(request,'otp.html')
        return HttpResponse('Password Not Verified')
    return render(request,'changepassword.html')



def otp(request):
    if request.method == 'POST':
        UOTP=request.POST.get('otp')
        GOTP=request.session.get('otp')
        print(GOTP)
        if UOTP==str(GOTP):
            un=request.session.get('username')
            UO=User.objects.get(username=un)
            pw=request.session.get('pw')
            UO.set_password(pw)
            UO.save()
            return HttpResponse('Password Updated !!!')
        return HttpResponse('Invalid OTP...')
    return render(request,'otp.html')



def forgotpassword(request):
    if request.method == 'POST':
        un=request.POST.get('un')
        UO=User.objects.get(username=un)
        if UO:
            otp= randint(100000,999999)
            request.session['otp']=otp
            request.session['username']=un
            email=UO.email
            send_mail(
            'OTP for forgot password',
            f'OTP for the forgot password: {otp}',
            'piyushgamechanger5@gmail.com',
            [email],
            fail_silently=False
            )
            return render(request,'forgotpasswordotp.html')
        return HttpResponse('Username Not Verified')
    return render(request,'forgotpassword.html')



def forgotpasswordotp(request):
    if request.method == 'POST':
        UOTP=request.POST.get('otp')
        GOTP=request.session.get('otp')
        if UOTP==str(GOTP):
            return render(request,'updatepassword.html')
        return HttpResponse('Invalid OTP')
    return render(request,'fogotpasswordotp.html')



def updatepassword(request):
    if request.method == 'POST':
        pw=request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            un=request.session.get('username')
            UO=User.objects.get(username=un)
            UO.set_password(pw)
            UO.save()
            return render(request,'master_login.html')
        return HttpResponse('Password Not Matched')
    return render(request,'updatepassword.html')




def master_items(request):
    EIFO=ItemForm()
    d={'EIFO':EIFO}
    if request.method=='POST' and request.FILES:
        IFDO=ItemForm(request.POST,request.FILES)
        if IFDO.is_valid():
            IFDO.save()
            return HttpResponse('Item Added Successfully')
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
    EIFO=ItemForm(instance=get_menu)
    d={'EIFO':EIFO}
    if request.method=='POST':
        IFDO=ItemForm(request.POST,instance=get_menu)
        if IFDO.is_valid():
            IFDO.save()
            return HttpResponseRedirect(reverse('menu'))
    return render(request,'mastermenu_update.html',d)