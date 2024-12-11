from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import requests


# Global variables
api_url = 'http://backend-fastapi:5001'  
menu_path = {'home':'/home',
             'dashboard':'/dashboard',
             'machinelearning':'/machinelearning',
             'scorecard': '/scorecard',
             'yolov5':'/yolov5',
             'demo404':'/demo404',
             'processing':'/processing'}
loan_purpose = ["car", "credit_card", "debt_consolidation",
                "educational", "home_improvement", "house",
                "major_purchase", "medical", "moving",
                "renewable_energy", "small_business","vacation",
                "wedding", "other"]


# User-defined functions
def update_dashboard_data(api_url):        
    try:       
        all_years = requests.get(api_url+"/api/all_years").json()           
        postdata = {"yyyy": all_years[0]}  
    except:        
        print("--- Error when getting all_years ---")        
        dicts = {"all_years": ""}
        items = ['loan_amt','loan_count','default_amt','default_count','month_loan','month_count','purpose','occupation']  
        for item in items:
            dicts[item] = ""
    else:        
        dicts = {"all_years": all_years}
        items = ['loan_amt','loan_count','default_amt','default_count','month_loan','month_count','purpose','occupation']  
        for idx, item in enumerate(items):        
            item_data = requests.post(api_url+"/api/"+item, json=postdata).json()
            if idx < 4:
                for k, v in item_data.items():
                    item_data[k] = format(v, ',')
            dicts[item]=item_data     
    return dicts  
    
   
# Create your views here.
def index(request):
    return redirect('/login')
    

def login(request):    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/home')      
    return render(request, 'login.html', locals())    
      

def log_out(request):
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_name = request.user
    auth.logout(request)
    return render(request, 'log_out.html', {
        'user_name': user_name, 'dt': dt
    })


@login_required
def home(request): 
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_name = request.user
    return render(request, 'home.html', {        
        'now': dt,
        'title': '首頁',
        'menu': menu_path,
        'user_name': user_name,
    })


@login_required
def dashboard(request): 
    dicts = update_dashboard_data(api_url)                
    dicts['now'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dicts['title'] = '資料視覺化分析'
    dicts['menu'] = menu_path
    dicts['user_name'] = request.user    
    return render(request, 'dashboard.html', dicts)
    

@login_required
def ml(request):
    return render(request, 'ml.html', {                
        'title': '機器學習',
        'menu': menu_path,
        'user_name': request.user,
    })


@login_required
def scorecard(request):
    return render(request, 'scorecard.html', {                
        'title': '信用評分預測',
        'menu': menu_path,
        'user_name': request.user,
        'loan_purpose': loan_purpose,
    })


@login_required
def yolov5(request):
    return render(request, 'yolov5.html', {                
        'title': '物件檢測',
        'menu': menu_path,
        'user_name': request.user,
    })


@login_required
def demo404(request):
    return render(request, '404.html', {                
        'title': 'Page Test',
        'menu': menu_path,
        'user_name': request.user,
    })


@login_required
def processing(request):
    return render(request, 'processing.html', {                
        'title': '違約分析',
        'menu': menu_path,
        'user_name': request.user,
    })
