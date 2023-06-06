from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from .models import patient_data
from django.contrib.auth.decorators import login_required


import  pandas as pd
import joblib

# @login_required(login_url='login')
def index(request):
    return render(request,"index.html")


def register(request):
    if request.method=='POST':
        print(request.user)
        fname=request.POST.get('first_name')
        lname=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password_repeat=request.POST.get('password_repeat')
        if password==password_repeat:
            if User.objects.filter(username=username).exists():
                messages.warning(request,"User name already exists!!")
                return render(request,"register.html")
            elif User.objects.filter(email=email).exists():
                messages.warning(request,"Email already exists!!")
                return render(request,"register.html")
            else:    
                user=User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password)
                user.save()
                return render(request,"login.html")
        else:
            messages.warning(request,"Password Not Matching!!")
            return render(request,"register.html")
    else:
        return render(request,"register.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passw = request.POST['pass']
        user = auth.authenticate(username=username, password=passw)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect('login')

def inspection(request):
    if request.method=='POST':
        loaded_model = joblib.load(r"C:\Users\Dell\django_workspace\Diabetes_Prediction\logistic_regression_model.sav")
        val1=float(request.POST['n1'])
        val2=float(request.POST['n2'])
        val3=float(request.POST['n3'])
        val4=float(request.POST['n4'])
        val5=float(request.POST['n5'])
        val6=float(request.POST['n6'])
        val7=float(request.POST['n7'])
        val8=float(request.POST['n8'])
        input_data = pd.DataFrame([[val1,val2,val3,val4,val5,val6,val7,val8]], columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'])
        pred=loaded_model.predict(input_data)[0]
        print(pred)
        result1=""
        if pred==1:
            result1="Positive"
        else:
            result1="Negative"
        userid=request.user
        patient=patient_data.objects.create(Pregnancies=val1,GLucose=val2,Blood_Pressure=val3,Skin_Thickness=val4,Insulin=val5,BMI=val6,DPF=val7,Age=val8,Result=result1,user_id=userid.id)
        patient.save()
        # mailing
        getemail=list(User.objects.filter(id=request.user.id).values_list('email'))[0][0]
        send_mail(
            'Diabetes Test Result',
            'Result: '+result1,
            'te6900973@gmail.com',
            [getemail],
            fail_silently=False,\
        )
        messages.info(request,"test report sent your email")
        
        return render(request,"inspection.html")
    else:
        return render(request,'inspection.html')



## display data of prediction
def result(request):
    user=request.user
    data = patient_data.objects.filter(user=user).order_by('-id')[:5]
    return render(request,'results.html',{'data':data})

