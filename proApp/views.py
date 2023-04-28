from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from proApp import dbconnection
from proApp import prediction
from django.core.files.storage import FileSystemStorage
from datetime import date
import os
from werkzeug.utils import secure_filename
basepath = os.path.dirname(__file__)
# Create your views here.
def home(request):  
    qry1="select * from staff order by id desc"
    data=dbconnection.selectalldata(qry1)
    return render(request,'index.html',{'data':data})

def staff(request): 
    if request.method=='POST':
        u =request.POST.get("u") 
        pas =request.POST.get("pas")          
        qry="select * from login where uid='"+u+"' and pwd='"+pas+"'"
        data=dbconnection.selectdata(qry)   
        if data:
            utype=data[3]
            print(utype)
            if utype =="stf":
                request.session['u']=u
                return HttpResponseRedirect("http://127.0.0.1:8000/vein")
            else:
                request.session['x']=u
                return HttpResponseRedirect("http://127.0.0.1:8000/adminhome")
        else:
           return HttpResponseRedirect("http://127.0.0.1:8000/staff?error=1") 
    if request.GET.get("error"):
        x=1
    else:
        x=0     
    return render(request,'staff.html',{'x':x})

def vein(request):  
    uid=request.session['u']
    qry1="select * from staff where crid='"+uid+"'"
    data=dbconnection.selectdata(qry1)
    if request.method=='POST':
        up=request.FILES['up']
        fs=FileSystemStorage()
        filename=fs.save("proApp/static/login/"+up.name,up) 
        pr=prediction.load_image(up.name)
        print(pr[0])
        amt=round(float(pr[0])*100)
        print(amt)
        print(pr[1])
        if uid == pr[1]:
            return HttpResponseRedirect("http://127.0.0.1:8000/veinok?amt="+str(pr[0])) 
        else:
            return HttpResponseRedirect("http://127.0.0.1:8000/vein?error=1")  
    if request.GET.get("error"):
        error=1
    else:
        error=""
    return render(request,'vein.html',{'data':data,'error':error})

def veinok(request):  
    uid=request.session['u']
    amt=request.GET.get("amt")
    qry1="select * from staff where crid='"+uid+"'"
    data=dbconnection.selectdata(qry1)       
    return render(request,'veinok.html',{'data':data,'amt':amt})

def predicts(request): 
    pid =request.GET.get("pid") 
    pr=prediction.load_image(pid)
    print(pr[0])
    amt=round(float(pr[0])*100,2)
    print(amt)
    print(pr[1])
    qry1="select * from staff where id='"+pr[1]+"'"
    data=dbconnection.selectdata(qry1)
    return render(request,'predict.html',{'pid':pid,'data':data,'amt':amt})

def login(request):  
    if request.method=='POST':
        a=request.POST.get('uid')
        b=request.POST.get('pas')
        sql="select * from login where uid='"+a+"' and pwd='"+b+"'"
        data=dbconnection.logindata(sql)
        if data:                        
            if data[3]=="admin":
                request.session['x']=a
                return HttpResponseRedirect("http://127.0.0.1:8000/adminhome")
    return render(request,'login.html',{})

def adhome(request):
    qry1="select * from staff order by id desc"
    data=dbconnection.selectalldata(qry1)
    return render(request,'office/index.html',{'data':data})

def addfinger(request):
    if request.method=='POST':
        nme=request.POST.get('nme')
        cid=request.POST.get('cid')
        pas=request.POST.get('pas')
        crm=request.POST.get('crm')
        up=request.FILES['pic']
        f1=request.FILES['f1']
        f2=request.FILES['f2']
        f3=request.FILES['f3']
        f4=request.FILES['f4']
        f5=request.FILES['f5']
        f6=request.FILES['f6']
        f7=request.FILES['f7']
        f8=request.FILES['f8']
        f9=request.FILES['f9']
        f10=request.FILES['f10']
        path="proApp/static/fingerprint/"+cid
        if not os.path.exists(path):
            os.mkdir(path)
        fs=FileSystemStorage()
        filename=fs.save("proApp/static/staff/"+up.name,up)  
        fs.save("proApp/static/fingerprint/"+cid+"/"+f1.name,f1)
        fs.save("proApp/static/fingerprint/"+cid+"/"+f2.name,f2)
        fs.save("proApp/static/fingerprint/"+cid+"/"+f3.name,f3)
        fs.save("proApp/static/fingerprint/"+cid+"/"+f4.name,f4)
        fs.save("proApp/static/fingerprint/"+cid+"/"+f5.name,f5)
        fs.save("proApp/static/fingerprint/"+cid+"/"+f6.name,f6)
        fs.save("proApp/static/fingerprint/"+cid+"/"+f7.name,f7)
        fs.save("proApp/static/fingerprint/"+cid+"/"+f8.name,f8)
        fs.save("proApp/static/fingerprint/"+cid+"/"+f9.name,f9)
        fs.save("proApp/static/fingerprint/"+cid+"/"+f10.name,f10)
        qry="INSERT INTO `staff`(`nme`, `crid`, `crm`, `pic`, `f1`, `f2`, `f3`, `f4`, `f5`, `f6`, `f7`, `f8`, `f9`, `f10`) VALUES ('"+str(nme)+"','"+str(cid)+"','"+str(crm)+"','"+str(up)+"','"+str(f1)+"','"+str(f2)+"','"+str(f3)+"','"+str(f4)+"','"+str(f5)+"','"+str(f6)+"','"+str(f7)+"','"+str(f8)+"','"+str(f9)+"','"+str(f10)+"')"
        dbconnection.insertdata(qry)
        qry1="INSERT INTO `login`(`uid`, `pwd`, `typ`) VALUES ('"+cid+"','"+pas+"','stf')"
        dbconnection.insertdata(qry1)
    qry1="select * from staff order by id desc"
    data=dbconnection.selectalldata(qry1)
    return render(request,'office/addfinger.html',{'data':data})

def crdata(request):
    cid=request.GET.get('cid')
    qry1="select * from staff where crid='"+cid+"'"
    data=dbconnection.selectdata(qry1)
    return render(request,'office/crdata.html',{'data':data})

def logout(request):
    return HttpResponseRedirect("http://127.0.0.1:8000/")
