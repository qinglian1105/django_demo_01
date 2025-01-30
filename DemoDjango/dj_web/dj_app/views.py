from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import requests
import os


# Global variables
MENU_PATH = {
    "home": "/home",
    "dashboard": "/dashboard",
    "machinelearning": "/machinelearning",
    "scorecard": "/scorecard",
    "yolov5": "/yolov5",
    "demo404": "/demo404",
    "processing": "/processing",
}
LOAN_PURPOSE = [
    "car",
    "credit_card",
    "debt_consolidation",
    "educational",
    "home_improvement",
    "house",
    "major_purchase",
    "medical",
    "moving",
    "renewable_energy",
    "small_business",
    "vacation",
    "wedding",
    "other",
]
PREDICTORS = [
    "loan_amt",
    "loan_count",
    "default_amt",
    "default_count",
    "month_loan",
    "month_count",
    "purpose",
    "occupation",
]
load_dotenv(dotenv_path=".env.develop", override=True)
API_URL = os.environ.get("API_URL")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}", "accept": "application/json"}


# User-defined functions
def update_dashboard_data(api_url):
    try:
        all_years = requests.get(api_url + "/api/pg/all_years", headers=HEADERS).json()
        postdata = {"yyyy": all_years[0]}
    except:
        print("--- Error when getting all_years ---")
        dicts = {"all_years": ""}
        for predictor in PREDICTORS:
            dicts[predictor] = ""
    else:
        dicts = {"all_years": all_years}
        for idx, predictor in enumerate(PREDICTORS):
            item_data = requests.post(
                api_url + "/api/pg/" + predictor, headers=HEADERS, json=postdata
            ).json()
            if idx < 4:
                for k, v in item_data.items():
                    item_data[k] = format(v, ",")
            dicts[predictor] = item_data
    return dicts


# Create your views here.
def index(request):
    return redirect("/login")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/home")
    return render(request, "login.html", locals())


def log_out(request):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_name = request.user
    auth.logout(request)
    return render(request, "log_out.html", {"user_name": user_name, "dt": dt})


@login_required
def home(request):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_name = request.user
    return render(
        request,
        "home.html",
        {
            "now": dt,
            "title": "首頁",
            "menu": MENU_PATH,
            "user_name": user_name,
        },
    )


@login_required
def dashboard(request):
    dicts = update_dashboard_data(API_URL)
    dicts["now"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dicts["title"] = "資料視覺化分析"
    dicts["menu"] = MENU_PATH
    dicts["user_name"] = request.user
    return render(request, "dashboard.html", dicts)


@login_required
def ml(request):
    return render(
        request,
        "ml.html",
        {
            "title": "機器學習",
            "menu": MENU_PATH,
            "user_name": request.user,
        },
    )


@login_required
def scorecard(request):
    return render(
        request,
        "scorecard.html",
        {
            "title": "信用評分預測",
            "menu": MENU_PATH,
            "user_name": request.user,
            "loan_purpose": LOAN_PURPOSE,
        },
    )


@login_required
def yolov5(request):
    return render(
        request,
        "yolov5.html",
        {
            "title": "物件檢測",
            "menu": MENU_PATH,
            "user_name": request.user,
        },
    )


@login_required
def demo404(request):
    return render(
        request,
        "404.html",
        {
            "title": "Page Test",
            "menu": MENU_PATH,
            "user_name": request.user,
        },
    )


@login_required
def processing(request):
    return render(
        request,
        "processing.html",
        {
            "title": "違約分析",
            "menu": MENU_PATH,
            "user_name": request.user,
        },
    )
