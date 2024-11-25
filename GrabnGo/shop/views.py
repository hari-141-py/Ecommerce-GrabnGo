from django.shortcuts import render,HttpResponse,redirect
from shop.models import Category,Product,User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def home(request):
    k = Category.objects.all()
    return render(request,'home.html', {'category': k})

@login_required
def product_list(request,p):    #p receives category id
    c = Category.objects.get(id=p)  #to get particular category object using id
    p = Product.objects.filter(category=c)  #to read all the products under particular category object
    context = {'cat_id':c,'prd_list':p}
    return render(request,'product_list.html',context)

@login_required
def product_details(request,i):
    p = Product.objects.get(id=i)
    return render(request,'product_details.html',{"product":p})


def user_register(request):
    if (request.method == 'POST'):
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        uname = request.POST.get('username')
        pswrd = request.POST.get('password')
        cnfpswrd = request.POST.get('confpassword')
        if (pswrd == cnfpswrd):
            k = User.objects.create_user(username=uname, password=pswrd, first_name=fname, last_name=lname,email=email)
            k.save()
            return redirect('shop:user_login')
        else:
            return HttpResponse("Passwords not matching")
    return render(request,'user_register.html',{})

def user_login(request):
    if (request.method == 'POST'):
        uname = request.POST.get('u')
        pswrd = request.POST.get('p')
        user = authenticate(username=uname, password=pswrd)
        if user:
            login(request, user)
            return redirect('shop:home')
        else:
            return HttpResponse("Invalid User")

    return render(request,'user_login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return redirect('shop:user_login')

@login_required
def add_category(request):
    if(request.method == "POST"):
        cname=request.POST["cname"]
        cimg=request.FILES["cimg"]
        cdesc=request.POST["cdesc"]

        c=Category.objects.create(name=cname,desc=cdesc,image=cimg)
        c.save()
        return redirect("shop:home")
    return render(request,"add_category.html")

@login_required
def add_product(request):
    if (request.method == "POST"):
        pname = request.POST["pname"]
        pimg = request.FILES["pimg"]
        price = request.POST["price"]
        stock = request.POST["stock"]
        category = request.POST["category"]
        pdesc = request.POST["pdesc"]

        cat=Category.objects.get(name=category)

        p=Product.objects.create(name=pname,desc=pdesc,image=pimg,price=price,stock=stock,category=cat)
        p.save()
        return redirect("shop:home")

    return render(request,"add_product.html")

@login_required
def add_stock(request,p):
    product=Product.objects.get(id=p)
    if (request.method == "POST"):
        product.stock=request.POST['stock']
        product.save()
        return redirect("shop:home")
    return render(request,"add_stock.html",{"pro":product})






