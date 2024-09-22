from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django .http import HttpResponse
# import the message from the settings
from django .contrib import messages ,auth
from django .contrib.auth.decorators import login_required


# Create your views here.
# verification email
from django .contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
            auth.login(request,user)
            messages.success(request,'you have sucessfully logged in')
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
    return render(request,'account/dashboard.html')


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