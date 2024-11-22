from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,UserProfileForm,UserForm
from .models import Account,UserProfile
from orders.models import Order,OrderProduct
from django .http import HttpResponse
# import the message from the settings
from django .contrib import messages ,auth
from django .contrib.auth.decorators import login_required

from  carts .views import _cart_id
from carts.models import Cart , Cartitem
# Create your views here.
# verification email
from django .contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests

def register(request):
    if request .method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()

            # User Activation
            current_site= get_current_site(request)
            mail_subject='please activate your account'
            message=render_to_string('account/account_verification_email.html',{
            'user': user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject, message ,to=[to_email])
            send_email.send()
            # messages.success(request,'Registration successful')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form=RegistrationForm() 
    context={
        'form':form
    }
    return render(request,'account/register.html',context)


def login(request):
    # this get the  name email and name password in the login .html
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user= auth.authenticate(email=email,password=password)

        if user is not None:
            try:
          
              cart=Cart.objects.get(cart_id=_cart_id(request))
              is_cart_item_exists=Cartitem.objects.filter(cart=cart).exists()
              if is_cart_item_exists:
                   cart_item=Cartitem.objects.filter(cart=cart)
                   #setting the product variation by card_id
                   product_variation=[]
                   for item in cart_item:
                       variation=item.variations.all()
                       product_variation.append(list(variation))

              # get cart_item from the user to access his product variation
              cart_item=Cartitem.objects.filter( user=user)
              ex_var_list=[]
              id=[]
              for item in cart_item:
                    existing_variation= item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
              
              for pr in product_variation:
                  if pr in ex_var_list:
                    index=ex_var_list.index(pr)
                    item_id=id[index]
                    item=Cartitem.objects.get(id=item_id)
                    item.quantity +=1
                    item.user=user
                    item.save()
                  else:
                      cart_item=Cartitem.objects.filter(cart=cart)
                      for item in cart_item:
                        item.user= user
                        item.save()
            except:
                print ('is entering inside except block')
                pass
            auth.login(request,user)
            messages.success(request,'you have sucessfully logged in')
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                print('query->',query)
                params=dict(x.split('=')for x in query.split('&'))
                if 'next' in params:
                    nextpage=params['next']
                    return redirect(nextpage)
               
            except:
                 return redirect ('dashboard')
        else:
            messages.error(request,'invaid login credentails')
        return redirect('login')
        

    return render(request,'account/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('login')





def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'congratulations your account is activated' )
        return redirect('login')
    else :
        messages.error(request,'invaid activation link')
        return redirect('register')
        
    
@login_required(login_url = 'login')
def dashboard(request):
    orders=Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count= orders.count()
    userprofile=UserProfile.objects.get_or_create(user_id=request.user.id)
    #userprofile = UserProfile.objects.get_or_create(user=request.user)
    context ={
        'orders_count':orders_count,
        'userprofile': userprofile,
    }
    return render(request,'account/dashboard.html',context)


def forgotpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            # reset password email
            current_site= get_current_site(request)
            mail_subject='Reset your password'
            message=render_to_string('account/reset_password_email.html',{
            'user': user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject, message ,to=[to_email])
            send_email.send()
            messages.success(request,'password reset email has been sent to your email address')
            return redirect('login')
             
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotpassword')
       
    return render(request,'account/forgotpassword.html')


def resetpassword_vaildate (request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'The link has expired')
        return redirect('login')

    
    
def resetpassword(request):
    if request.method =='POST':
        password=request.POST['password']
        confirm_password=request.POST['password']
        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset succesful')
            return redirect('login')
        else:
            messages.error(request,'password do not match')
            return  redirect('resetpassword')
    else:
        return render(request,'account/resetpassword.html')
    


def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders,
    }

    return render(request,'account/my_orders.html',context)

@login_required(login_url = 'login')
def edit_profile (request):
    
    userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method=='POST':
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form .is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'your proflie has been updated')
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
    
    context={
        'user_form' :user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
        
    }

    return render(request,'account/edit_profile.html',context)

@login_required(login_url = 'login')
def changepassword(request):
    if request.method=='POST':
        current_password= request.POST['current_password']
        new_password= request.POST['new_password']
        confirm_password= request.POST['confirm_password']
        user=Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'password updated successfully.')
                return redirect('changepassword')
            else:
                messages.error(request,'please enter valid current password')
                return redirect('changepassword')
        else:
            messages.error(request,'password does not match')
            return redirect('changepassword')

    return render(request,'account/changepassword.html')

     
@login_required(login_url = 'login')
def order_details(request,order_id):
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    order= Order.objects.get(order_number=order_id)
    subtotal=0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context={
        'order_detail': order_detail,
        'order':order,
        'subtotal' : subtotal,
    }
    return render(request,'account/order_details.html',context)
   