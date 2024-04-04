from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from StyleSculptapp.models import Product,Cart,Order,History,Address
from django.db.models import Q
import razorpay,random
from django.core.mail import send_mail

# Create your views here.
def main(request):
    return render(request,'main.html')

def index(request):
    return render(request,'index.html')

def register(request):
    context={}
    if request.method=='GET':
        return render(request,'register.html')
    else:
        uname=request.POST['uname']
        email=request.POST['email']
        upass=request.POST['upass']
        cpass=request.POST['cpass']
       # add=request.POST['add']

        if uname=="" or email=="" or upass=="" or cpass=="" or add=="":
            #print("Fill all the details!")
            context['errmsg']="Fill all the details!"
            return render(request,'register.html',context)
        elif upass!=cpass:
            #print("Password & Confirm Password should be same")
            context['errmsg']="Password & Confirm Password should be same"
            return render(request,'register.html',context)

        elif len(upass)<8:
            #print("Password must be contain atleast 8 characters")
            context['errmsg']="Password must be contain atleast 8 characters"
            return render(request,'register.html',context)
        

        else:
            try:
                u=User.objects.create(username=uname,email=email)
                u.set_password(upass)
                u.save()
                #address = Address.objects.create(address=add, username=uname)
                context['success']="User Registered Successfully"
                #return HttpResponse("Registered Successfully")
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User already exsists. Please Login !"
                return render(request,'register.html',context)

def user_login(request):
    if request.method=="GET":
            return render(request,'login.html')
    else:
            uname=request.POST['uname']
            upass=request.POST['upass']
            date=request.POST['login']
            u=authenticate(username=uname,password=upass,last_login=login)
            if u is not None:
                login(request,u)
                return redirect('/index')
            else:
                context={}
                context['errmsg']="Invalid Details"

                return render(request,'login.html',context)
def user_logout(request):
    logout(request)
    return redirect('/index')

def about(request):
    return render(request,'about.html')

def product(request):
    p=Product.objects.filter(is_active=True)
    #print(p)
    context={}
    context['data']=p
    return render(request,'product.html',context)

def product_details(request,pid):
    p = Product.objects.filter(id=pid)
    context={}
    context['data']=p
    return render(request,'product_details.html',context)

def catfilter(request,cid):

    q1=Q(category=cid)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'product.html',context)

def sorting(request,sv):
    if sv=='1':
        p=Product.objects.order_by('price').filter(is_active=True)
    else:
        p=Product.objects.order_by('-price').filter(is_active=True)
    
    context={}
    context['data']=p
    return render(request,'product.html',context)

def filtering(request):
    min=request.GET['min']
    max=request.GET['max']

    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['data']=p
    return render(request,'product.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)

        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context['data']=p
        if n==1:
            context['errmsg']="Product is already added"
            return render(request,'product_details.html',context)
        else:    
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']='Product Added Successfully'
            return render(request,'product_details.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)

    sum=0
    for i in c:
        sum=sum+i.pid.price*i.quantity
    context={}
    context['data']=c
    context['total']=sum
    context['n']=len(c)
    return render(request,'cart.html',context)

def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def quantity(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].quantity
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1
    
    c.update(quantity=q)
    return redirect('/viewcart')

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    for i in c:
        amount=i.pid.price*i.quantity
        o=Order.objects.create(uid=i.uid,pid=i.pid,quantity=i.quantity,amt=amount)
        o.save()
        i.delete()
    return redirect('/fetchorder')

def history(request):
    o=Order.objects.filter(uid=request.user.id)
    for i in o:
        amount=i.pid.price*i.quantity
        h=History.objects.create(uid=i.uid,pid=i.pid,quantity=i.quantity,amt=amount)
        h.save()
        i.delete()
    history = History.objects.all()
    return render(request, 'order_history.html', {'history': history})

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    context={}
    sum=0
    for i in o:
        sum=sum+i.amt
    context['total']=sum
    context['data']=o
    context['n']=len(o)
    return render(request,'placeorder.html',context)

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_aGx3kBGexBmrlf", "4aYniVp59iZWG5qOT0jSOGY2"))
    oid=random.randrange(1000,9999)
    o=Order.objects.filter(uid=request.user.id)
    sum=0
    for i in o:
        sum=sum+i.amt
    data = { "amount": sum*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    context={}
    context['payment']=payment
    return render(request,'payment.html',context)

def payment_success(request):
    sub="StyleSculpt Order Status"
    msg="Thanks for Shopping !! \n Continue with your Dream and get your DreamOutfit customized with us"
    frm='sejukhushi30@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    send_mail(
        sub,msg,frm,[to],fail_silently=False
    )
    return render(request,'payment_success.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        
        sub = 'Contact Form Submission'
        to='khushboooswal25@gmail.com'
        u=User.objects.filter(id=request.user.id)
        frm=u[0].email
        msg= (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Message: {message}\n"
            f"Appointment Date: {appointment_date}\n"
            f"Appointment Time: {appointment_time}\n"
        )

        send_mail(sub,msg,frm,[to],fail_silently=False)
        return render(request, 'success.html')
    else:
        return render(request, 'contact.html')