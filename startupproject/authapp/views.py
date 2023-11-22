from django.shortcuts import render,redirect
from django.contrib import messages
import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import View 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from authapp.utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings



# Create your views here.
def signup(request):
    flag=0
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password Not matching")
            return redirect('/auth/signup/')
        if len(password)<=8:
            messages.warning(request,"Password must be atleast 8 character")
            return redirect('/auth/signup/')
        elif not re.search("[a-z]",password):
            flag = -1
        elif not re.search("[A-Z]",password):
            
            flag = -1
        elif not re.search('[0-9]',password):
            flag = -1
        elif not re.search('[_@$#%*()-]',password):
            flag= -1
        else:
            pass
        if (flag==0):
            try :
                if User.objects.get(username=email):
                    messages.info(request,"Email is Taken")
                    return redirect('/auth/signup/')
            except Exception as identifier:
                pass
            user=User.objects.create_user(email,email,password)
            user.first_name=name
            user.is_active=False
            
            user.save()
            email_subject="Activate Your Account"
            message=render_to_string('activate.html',{
                'user':user,
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)

            })
            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()
            messages.success(request,"Activate your Account by clicking the Link in your gmail")
            return redirect('/auth/login/')
        else:
            messages.error(request,"Password is not Valid")
            return redirect('/auth/signup/')
                
              
        
        
    return render(request,'signup.html')


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/auth/login/')
        return render(request,'activatefail.html')


def handlelogin(request):
     if request.method=="POST":
        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/auth/login/')

     return render(request, "login.html")
    
        
    

def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return render(request,'login.html')


class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')

    def post(self,request):

        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            # current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()
            messages.info(request,"Clicking the link send to your Register Email to Reset the Password " )
            return render(request,'request-reset-email.html')
        else:
            messages.error(request,'No Account Exists with this email' )
            return render(request,'request-reset-email.html')    



class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        flag = 0
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'set-new-password.html',context)
        
        if len(password)<=8:
            messages.warning(request,"Password must be atleast 8 character")
            return render(request,'set-new-password.html',context)
        elif not re.search("[a-z]", password):
            flag = -1
            
        elif not re.search("[A-Z]", password):
            flag = -1
            
        elif not re.search("[0-9]", password):
            flag = -1
            
        elif not re.search("[_@$]" , password):
            flag = -1  
        else:
            pass


       
        if(flag==0):  
            try:
                user_id=force_text(urlsafe_base64_decode(uidb64))
                user=User.objects.get(pk=user_id)
                user.set_password(password)
                user.save()
                messages.success(request,"Password Reset Success Please Login with NewPassword")
                return redirect('/')

            except DjangoUnicodeDecodeError as identifier:
                messages.error(request,"Something Went Wrong")
                return render(request,'set-new-password.html',context)

  
    
    