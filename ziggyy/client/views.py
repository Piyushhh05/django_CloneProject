from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from client.forms import *
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from master.models import *
from django.core.mail import send_mail
from random import randint
from django.contrib.auth.decorators import login_required
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



@login_required
def client_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



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
            return render(request,'client_login.html')
        return HttpResponse('Password Not Matched')
    return render(request,'updatepassword.html')



def client_menu(request,type):
    if type=='veg':
        items=Items.objects.filter(items_type='Veg')
    elif type=='non-veg':
        items=Items.objects.filter(items_type='Non-Veg')
    elif type=='refreshment':
        items=Items.objects.filter(items_type='Refreshment')    
    elif type=='all':
        items=Items.objects.all()
    d={'items':items}
    return render(request,'client_menu.html',d)


   
    

def cart(request):
    CO=Cart.objects.all()
    un=request.session['username']
    CCI=list(filter(lambda i: i.cart_id.username==un,CO))
    Grand_Total=0
    for i in CCI: 
        i.total=i.quantity*i.price
        Grand_Total+=i.total
    d={'items':CCI,'Grand_Total':Grand_Total}
    return render(request,'cart.html',d)


def addtocart(request):
    if request.method == 'POST':
        items_pk = request.POST.get('itempk')
        items_object = Items.objects.get(items_id=items_pk)
        UO = User.objects.get(username = request.session['username'])
        name = items_object.items_name
        price = items_object.items_price
        quantity = request.POST.get('qty')
        
        CO = Cart(cart_id=UO, name=name, price=price, quantity=quantity, inst='')
        CO.save()
        return HttpResponse('Added to Cart')
    return HttpResponseRedirect(reverse('menu'))



def Buy(request):
    CO=Cart.objects.all()
    un=request.session['username']
    if CO:
        CCI=list(filter(lambda i: i.cart_id.username==un,CO))
        for i in CCI:
            i.delete()
            return HttpResponse('Order Placed Successfully')
    else:
        return HttpResponse('You have not add anything to the cart yet !!! ')