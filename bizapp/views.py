import uuid
import random
import string
import requests
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import SignupForm,UpdateForm
from .models import Product, Category,ProfileDetail,ShopCart,PaidOrder

# Create your views here.
def index(request):
    featured = Product.objects.filter(featured=True)
    latest = Product.objects.filter(new_arrival=True)

    context={
        'featured':featured,
        'latest':latest
    }

    return render(request, 'index.html',context) 


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }

    return render(request, 'categories.html',context) 


def all_products(request):
    all_products = Product.objects.all()
    
    context = {
        'products': all_products,
    }
    return render(request, 'all_products.html', context)


def product_category(request,id):
    single = Product.objects.filter(category_id=id)
    categories = Category.objects.all()

    context = {
        'single':single,
        'categories':categories
    }
    return render(request, 'prod_cat.html',context)


def product_detail(request,id):
    detail = Product.objects.get(pk=id)

    context = {
        'detail':detail
    }
    return render(request, 'detail.html',context)


# Authentication defined 
def loginform(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Ensure username/password is correct')
            return redirect('loginform')

    return render(request, 'login.html')


def logoutform(request):
   logout(request)
   return redirect('loginform')

def signupform(request):
    regform = SignupForm()
    if request.method == 'POST':
        regform = SignupForm(request.POST) 
        if regform.is_valid():
            reg = regform.save()
            newreg = ProfileDetail(user=reg)
            newreg.save()
            login(request, reg)
            messages.success(request, 'Your signup is successful')
            return redirect('index')
        else:
            messages.warning(request, regform.errors)
            return redirect('signupform')

    context = {
        'regform':regform
    } 

    return render(request, 'signup.html', context)

# Authentication  done

# profile 
@login_required(login_url='loginform')
def profile(request):
    profile = ProfileDetail.objects.get(user__username= request.user.username)

    context = {
        'profile':profile
    }

    return render(request, 'profile.html', context)


@login_required(login_url='loginform')
def update(request):    # user profile update 
    updateform = UpdateForm()
    if request.method == 'POST':
        updateform = UpdateForm(request.POST, request.FILES, instance=request.user.profiledetail)
        if updateform.is_valid():
            updateform.save()
            messages.success(request, 'Profile update successful')
            return redirect('profile')

    context = {
        'updateform':updateform
    }

    return render(request, 'update.html', context)


# password change
@login_required(login_url='loginform')
def password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)  
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password change successful')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('password')

    context = {
        'form':form
    }

    return render(request, 'password.html', context)
# profile done



# shortcart function 
@login_required(login_url='loginform')
def shopcart(request):
    if request.method == 'POST':
        quant = int(request.POST['quantity'])
        dpid = request.POST['pid']
        apid = Product.objects.get(pk=dpid)
        cart = ShopCart.objects.filter(paid_order=False, user__username= request.user.username)
        if cart:
            prod = ShopCart.objects.filter(user__username=request.user.username,product=apid.id).first()
            if prod:#check if product is in the cart...
                prod.quantity += quant  #if in the cart, increment quantity
                prod.save()
                messages.success(request, 'Product added to Cart!')
                return redirect('products')
            
            else:# add new item in the cart
                newitem = ShopCart()
                newitem.user = request.user
                newitem.product = apid
                newitem.quantity = quant
                newitem.cart_code = cart[0].cart_code #first index of the cart_code created
                newitem.paid_order = False
                newitem.save()

        else:
            order_number= str(uuid.uuid4())
            newcart = ShopCart()
            newcart.user = request.user
            newcart.product = apid
            newcart.quantity = quant
            newcart.cart_code = order_number
            newcart.paid_order = False
            newcart.save()

        messages.success(request, 'Product added to Cart!')
    return redirect('products')



#display items selected by individual shopper
@login_required(login_url='loginform')
def cart(request):
    cart = ShopCart.objects.filter(paid_order=False, user__username= request.user.username)

    total = 0
    vat = 0
    grand_total = 0

    for item in cart:
       total += item.product.price * item.quantity  

    vat = 0.075 * total

    grand_total = total + vat


    context ={
        'cart':cart,
        'total': total,
        'vat': vat,
        'grand_total': grand_total,
    }
    
    
    return render(request, 'cart.html', context)



# increase quantity of items 
@login_required(login_url='loginform')
def increase(request):
    increase = request.POST['addup']
    itemid = request.POST['itemid']
    newquantity = ShopCart.objects.get(pk=itemid)
    newquantity.quantity = increase
    newquantity.save()
    messages.success(request, 'Item quantity is updated')
    return redirect('cart')


#delete item from shopcart
@login_required(login_url='loginform')
def remove(request):
    remove = request.POST['del']
    ShopCart.objects.filter(pk=remove).delete()
    messages.success(request, 'Item sucessfully deleted from your cart')
    return redirect('cart') 



#display items selected by individual shopper
@login_required(login_url='loginform')
def checkout(request):
    cart = ShopCart.objects.filter(paid_order=False, user__username= request.user.username)
    profile = ProfileDetail.objects.get(user__username=request.user.username)

    total = 0
    vat = 0
    grand_total = 0

    for item in cart:
       total += item.product.price * item.quantity  

    vat = 0.075 * total

    grand_total = total + vat

    context ={
        'cart':cart,
        'grand_total': grand_total,
        'profile':profile,
        'order_code':cart[0].cart_code
    }
    
    return render(request, 'checkout.html', context)


#Integrating to paystack API
@login_required(login_url='loginform')
def paidorder(request):
    #collecting data for paystack use
    api_key = 'sk_test_0c3bb25f14513ee95dcbe057e8b007f8b8480aa1'
    curl = 'https://api.paystack.co/transaction/initialize'
    cburl = 'http://52.15.142.87/completed/'
    total = float(request.POST['gtotal']) * 100
    order_num = request.POST['order_no']
    ref_num = ''.join(random.choices(string.digits + string.ascii_letters, k=8))
    user = User.objects.get(username= request.user.username)

    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'reference': ref_num, 'amount':total, 'order_number':order_num, 'callback_url':cburl, 'email':user.email,'currency':'NGN'}
    #collecting data for paystack use ends here

    #call is now initaited to paystack
    try:
        r = requests.post(curl, headers=headers, json=data)#transaction successful then else block will be excuted
    except Exception:
        messages.error(request, 'Network busy, refresh your page and try again. Thank you!')
        #the exception block will hold brief incase transaction got an error
    else:
        transback = json.loads(r.text)#at this point its clear transaction was successful
        rd_url = transback['data']['authorization_url']
        paid = PaidOrder()
        paid.user= user
        paid.total_paid = total
        paid.cart_code = order_num
        paid.transac_code = ref_num
        paid.paid_order = True
        paid.first_name = user.profiledetail.first_name
        paid.last_name = user.profiledetail.last_name
        paid.phone= user.profiledetail.phone
        paid.address= user.profiledetail.address
        paid.city= user.profiledetail.city
        paid.state= user.profiledetail.state
        paid.save()

        #once items are taken out, the basket should become empty. To ensure this querry the ShopCart
        basket = ShopCart.objects.filter(user__username= request.user.username,paid_order=False)
        for item in basket:
            item.paid_order= True
            item.save()

            #once items are sold out, take inventory. To ensure this querry the Product
            stock = Product.objects.get(pk=item.product.id)
            stock.max_quantity -= item.quantity
            stock.save()

        return redirect(rd_url)  
    return redirect('checkout')


@login_required(login_url='loginform')
def completed(request):
    profile = ProfileDetail.objects.get(user__username=request.user.username)

    return render(request, 'completed.html', {'profile':profile}) 