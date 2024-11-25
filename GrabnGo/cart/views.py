from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart,Payment,Order_details
from shop.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import login
import razorpay

@login_required
def add_to_cart(request,i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        c = Cart.objects.get(product=p,user=u) #checks product in cart table for a particular user
        if(p.stock>0):  #checks if product is available or out of stock
            c.quantity+=1 #if present it will increment the quantity of the product
            c.save()
            p.stock-=1
            p.save()

    except:         #if not present it will create a new record inside the cart table with quantity = 1
        if (p.stock > 0):   #checks if product is available or out of stock
            c = Cart.objects.create(product=p,user=u,quantity=1)
            c.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cart_view')

@login_required
def remove_from_cart(request,i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        c=Cart.objects.get(user=u ,product=p)
        if(c.quantity>1):
            c.quantity-=1
            c.save()
            p.stock+=1
            p.save()

        else:
            c.delete()
            p.stock += 1
            p.save()
    except:
        pass

    return redirect('cart:cart_view')

@login_required
def delete_item_cart(request, i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        c = Cart.objects.get(user=u,product=p)
        c.delete()
        p.stock += c.quantity
        p.save()
    except:
        pass
    return redirect('cart:cart_view')

@login_required
def cart_view(request):
    u=request.user

    subtotal=0
    total = 0
    c = Cart.objects.filter(user=u)  # All cart items of a particular user
    for i in c:
        subtotal+=i.quantity * i.product.price
    # Only add shipping and tax if there are items in the cart
    if subtotal > 0:
        total = subtotal + 10 + 30  # Add shipping and tax
    else:
        total = subtotal  # No extra charges if the cart is empty

    return render(request,"cart_view.html",{'cart':c,'subtotal':subtotal,'total':total})

@login_required
def orderform(request):
    if(request.method=="POST"):
        address=request.POST.get('adrs')
        phoneno=request.POST.get('phno')
        pin=request.POST.get('pin')
        u=request.user
        c=Cart.objects.filter(user=u)
        subtotal=0
        for i in c:
            subtotal+=i.quantity*i.product.price
        total=subtotal + 10 + 30
        total=int(total*100)

        client = razorpay.Client(auth=('rzp_test_XdHXdgNheiw7SN','1EYvJLBvAXW7UjFj2XQ0tk5b'))   #Creates a Client connection using razorpay id and secret code

        order_data = {
            "amount": total,  # Amount in the smallest currency unit (e.g., paise for INR)
            "currency": "INR",
        }

        response_payment=client.order.create(data=order_data)   # Creates an order using Razorpay Client

        # print(response_payment)

        order_id=response_payment['id']
        order_status=response_payment['status']
        if(order_status=='created'):
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_details.objects.create(product=i.product,user=u,no_of_items=i.quantity,address=address,phoneno=phoneno,pin=pin,order_id=order_id)
                o.save()
        else:
            pass
        response_payment["name"]=u.username #additional information
        context={'payment':response_payment}
        return render(request,"payment.html",context)
    return render(request,"orderform.html")


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def payment_status(request,u):
    current_user = User.objects.get(username=u)
    if(not request.user.is_authenticated):
        login(request,current_user)
    if(request.method=="POST"):
        response=request.POST

        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
        client=razorpay.Client(auth=('rzp_test_XdHXdgNheiw7SN','1EYvJLBvAXW7UjFj2XQ0tk5b'))
        try:
            status=client.utility.verify_payment_signature(param_dict)
            print(status)

            #to retreive a particular record in payment table whose order_id matches the response order_id
            p=Payment.objects.get(order_id=response['razorpay_order_id'])
            p.razorpay_payment_id=response['razorpay_order_id']   #add payment id after succesfull completion
            p.paid=True #changes paid status to true
            p.save()


            o=Order_details.objects.filter(user=current_user,order_id=response['razorpay_order_id'])#retreives records in order detail matching with current user and response order id
            for i in o:
                i.payment_status="paid"
                i.save()

            c=Cart.objects.filter(user=current_user)    #after pay deleting items from cart
            c.delete()

        except:
            pass
    return render(request,"payment_status.html",{"status":status})


@login_required
def order_view(request):
    u=request.user
    o=Order_details.objects.filter(user=u,payment_status="paid")

    return render(request,"order_view.html",{"orders":o})















