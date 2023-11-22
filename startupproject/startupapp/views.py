from django.shortcuts import render,redirect
from authapp.models import Contact
from django.contrib import messages
from .models import Courses,Register,Payments,Attendance

from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.core.mail.message import EmailMessage

# Create your views here.
def index(request):
    return render(request,"index.html")
def about(request):
    return render(request,"about.html")
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phoneNo=request.POST.get('num')
        desc=request.POST.get('desc')
        query=Contact(name=name,email=email,phoneNumber=phoneNo,description=desc)
        query.save()
        from_email=settings.EMAIL_HOST_USER
        from_password=settings.EMAIL_HOST_PASSWORD
        connection=mail.get_connection()
        connection.open()
        email_message=mail.EmailMessage(f'Email from {name}', f'UserEmail: {email}\nUserPhoneNumber:{phoneNo}\n\n\n QUERY:{desc}',from_email,['yogeshbaghel8130@gmail.com',],connection=connection)
        
        email_client=mail.EmailMessage(f'Yogesh Baghel Response','Thnaks For Reaching Us\n\nName: Yogesh baghel\nContact : 8130135305\nEmail:yogeshbaghel8130@gmail.com',from_email,[email],connection=connection)
        connection.send_messages([email_message,email_client])
        connection.close()
        
        
        messages.info(request,"Thanks for contact me! we will get back you soon....")
        
        return render(request,"contact.html")
    
            
        
    return render(request,"contact.html")




def courses(request):
    courses=Courses.objects.all()
    context={"courses":courses}
    return render(request,"courses.html",context)

def course(request,id):
    course=Courses.objects.filter(courseName=id)
    context={"course":course}
    return render(request,"course.html",context)


def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login & Register With us")
        return redirect("/auth/login/")
    courses=Courses.objects.all()
    context={"courses":courses}
    
# if form submitted
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        fatherName=request.POST.get('fatherName')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        college=request.POST.get('college')
        addr=request.POST.get('addr')
        landmark=request.POST.get('landmark')
        street=request.POST.get('street')
        pcode=request.POST.get('pcode')
        city=request.POST.get('city')
        companyname=request.POST.get('companyname')
        Designation=request.POST.get('Designation')
        Qualification=request.POST.get('Qualification')
        cknowledge=request.POST.get('cknowledge')
        scourse=request.POST.get('scourse')
        ccourse=request.POST.get('ccourse')
        emailPresent=Register.objects.filter(email=email)
        if emailPresent:
            messages.error(request,"Email is already Taken")
            return redirect('/enroll/')

        if scourse==ccourse:
            pass
        else:
            messages.error(request,"Please Select the Valid Course...")
            return redirect('/enroll/')
        query=Register(firstName=fname,lastName=lname,fatherName=fatherName,phoneNumber=phone,email=email,collegeName=college,address=addr,landmark=landmark,street=street,city=city,pincode=pcode,companyName=companyname,designation=Designation,qualification=Qualification,computerKnowledge=cknowledge,Course=scourse)
        
        query.save()
        messages.success(request,"Enrollment Success")
        return redirect('/candidateprofile/')



    

    
    
    return render(request,"enroll.html",context)




def candidateprofile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login & View Your Profile")
        return redirect("/auth/login/")
    currentuser=request.user.username
    details=Register.objects.filter(email=currentuser)
    print(currentuser)
    payment=Payments.objects.all()
    paymentstatus=""
    amount=0
    balance=0
    for j in payment:
        if str(j.name)==currentuser:
            paymentstatus=j.status
            amount=j.amountPaid
            balance=j.balance
    paymentstats={"paymentstatus":paymentstatus,"amount":amount,"balance":balance}
    attendanceStats=Attendance.objects.filter(email=currentuser)  
    context={"details":details,"status":paymentstats, "attendanceStats":attendanceStats}
    

    return render(request,"profile.html",context)



def candidateupdate(request,id):
    data=Register.objects.get(candidateId=id)
    courses=Courses.objects.all()
    context={"data":data,"courses":courses}
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        fatherName=request.POST.get('fathername')
        phone=request.POST.get('phone')
        college=request.POST.get('college')
        addr=request.POST.get('addr')
        landmark=request.POST.get('landmark')
        street=request.POST.get('street')
        pcode=request.POST.get('pcode')
        city=request.POST.get('city')
        compnyname=request.POST.get('companyname')
        Designation=request.POST.get('Designation')
        Qualification=request.POST.get('Qualification')
        scourse=request.POST.get('scourse')
        
        edit=Register.objects.get(candidateId=id)
        edit.firstName=fname
        edit.lastName=lname
        edit.fatherName=fatherName
        edit.phoneNumber=phone
        edit.collegeName=college
        edit.address=addr
        edit.landmark=landmark
        edit.street=street
        edit.city=city
        edit.pincode=pcode
        edit.companyName=compnyname
        edit.designation=Designation
        edit.qualification=Qualification
        edit.Course=scourse
        edit.save()
        messages.info(request,"Data Update Successfully....")
        return redirect("/candidateprofile/")
    return render(request,"updatecandidate.html",context)


def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login & Aplly Attendance")
        return redirect("/auth/login/")
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        date=request.POST.get('date')
        logintime=request.POST.get('logintime')
        logouttime=request.POST.get('logouttime')
        query=Attendance(name=name,email=email,date=date,logintime=logintime,logouttime=logouttime)
        query.save()
        messages.success(request,"Applied Successfully wait for the approval ....")
        return redirect("/candidateprofile/")

    
    return render(request,"attendance.html")




def search(request):
    query=request.GET.get('search','')
    if len(query)>100:
        allPosts=Courses.objects.none()
    else:
        allPosts=Courses.objects.filter(courseName__icontains=query)
    if allPosts.count()==0:
        messages.warning(request,"No Search Results")
    params={'allPosts':allPosts,'query':query}
    return render(request,"search.html",params)