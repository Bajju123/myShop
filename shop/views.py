from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . models import user_reg, Category,Product
from cart.forms import CartAddProductForm
from django.contrib import messages
from django.contrib.messages import get_messages
import re
from django.db.models import Q

# Create your views here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')
CONTACT_REGEX = re.compile(r'^[0-9]')
CONTACT_REGEXX = re.compile(r'^[1-9]{1}[0-9]{9}')

def index(request):
    return render(request, 'shop/index.html')

def register(request, category_slug= None):

    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')

        if len(email) < 1:
            messages.add_message( request, messages.ERROR, "Email is required!")

        if not EMAIL_REGEX.match( email ):
            messages.add_message(request, messages.ERROR, "Invalid email format! Ex: test@text.com")

        if not CONTACT_REGEX.match( contact ):
            messages.add_message(request, messages.ERROR, "Invalid Contact format!!!")

        if not CONTACT_REGEXX.match( contact ):
            messages.add_message(request, messages.ERROR, "Contact must be 10 digit numbers!!!")

        if len(pwd1) < 8:
            messages.add_message(request, messages.ERROR, "Password must be between 8-32 character!")

        if pwd1 != pwd2:
            messages.add_message(request, messages.ERROR, "Password and Confirm Password must match!")

        if user_reg.objects.filter(email=email).count() > 0:
            messages.add_message(request, messages.ERROR, "A user with this email is already exists!")

        if user_reg.objects.filter(uname=uname).count() > 0:
            messages.add_message(request, messages.ERROR, "A user with this user name is already exists!")

        if len(get_messages(request)) > 0:
            msg = get_messages(request)
            return render(request, 'reg_login/register.html', {'msg': msg})

        else:

            reg1 = user_reg(fname=fname, lname=lname, uname=uname, contact_info=contact, email=email, gender=gender, pwd1=pwd1)
            reg1.save()

            category = None
            categories = Category.objects.all()
            products = Product.objects.filter(available=True)

            if category_slug:
                category = get_object_or_404(Category, slug=category_slug)
                products = products.filter(category=category)

            return render(request, 'shop/products/list.html', {'category': category,
                                                               'categories': categories,
                                                               'products': products})

    else:
        return render(request, 'reg_login/register.html')


def login(request, category_slug= None):
    username = 'not logged in'
    if request.method == "POST":

        name = request.POST.get('login_uname')
        pwd = request.POST.get('login_pwd')

        try:

            check_uname = user_reg.objects.filter(uname=request.POST['login_uname'])[0]
            check_pwd = user_reg.objects.filter(pwd1=request.POST['login_pwd'])[0]

            if name == check_uname.uname and pwd == check_pwd.pwd1:

                    username = name
                    request.session['username'] = username

                    category = None
                    categories = Category.objects.all()
                    products = Product.objects.filter(available=True)

                    if category_slug:
                        category = get_object_or_404(Category, slug=category_slug)
                        products = products.filter(category=category)


                    return render(request, 'shop/products/list.html', {'category': category,
                                                                       'categories': categories,
                                                                       'products': products,
                                                                       'username':username})

            else:
                return render(request, 'reg_login/login.html')


        except:
            messages.add_message(request, messages.ERROR, "Invalid UserName or Password !!")

            if len(get_messages(request)) > 0:
                msg = get_messages(request)
                return render(request, 'reg_login/login.html', {'msg': msg})

            return render(request, 'reg_login/login.html')

    else:
        return render(request, 'reg_login/login.html')

def logout(request, category_slug= None):
    try:
        del request.session['username']
        loggedout ='You are now logged out !'
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        return render(request, 'shop/products/list.html', {'category': category,
                                                           'categories': categories,
                                                           'products': products,
                                                           'username': loggedout})
    except:
        pass






def product_list(request, category_slug= None):

    if request.session.has_key('username'):
        username = request.session['username']
        un = username



    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/products/list.html', {'category': category,
                                                  'categories': categories,
                                                  'products': products})



def department(request, category_slug= None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/products/departments.html', {'category': category,
                                                  'categories': categories,
                                                  'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    return render(request, 'shop/products/detail.html',
                  {'product': product,
                   'cart_product_form':cart_product_form})

def about(request):

    return render(request, 'shop/ExtraPages/aboutus.html')

def contact(request):

    return render(request, 'shop/ExtraPages/contactus.html')

def tracker(request):
    return HttpResponse("This is Tracker page of Shop")


def search(request, category_slug= None):
    query = request.GET.get('search')

    if request.session.has_key('username'):
        username = request.session['username']
        un = username

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(Q(name__icontains=query) | Q(price__icontains=query) | Q(description__icontains=query) )

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/ExtraPages/search.html', {'category': category,
                                                  'categories': categories,
                                                  'products': products})



def productView(request):
    return HttpResponse("This is Product View page of Shop")

def checkout(request):
    return HttpResponse("This is Check Out page of Shop")
