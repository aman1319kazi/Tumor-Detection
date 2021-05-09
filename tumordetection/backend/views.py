from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os
import cv2
import numpy as np
import joblib
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

ROWS = 64
COLS = 64
CHANNELS = 3

data = joblib.load(os.path.join(BASE_DIR,'backend/model_joblib.pkl'))

def read_image(file_path):
    img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    return cv2.resize(img, (ROWS, COLS), interpolation=cv2.INTER_CUBIC)

def sigmoid(z):
    s = 1/(1+np.exp(-z))
    return s

def predict(w, b, X):    
    m = X.shape[1]
    Y_prediction = np.zeros((1, m))
    w = w.reshape(X.shape[0], 1)
    
    z = np.dot(w.T, X) + b
    A = sigmoid(z)
    
    for i in range(A.shape[1]):
        # Convert probabilities A[0,i] to actual predictions p[0,i]
        if A[0,i] > 0.5:
            Y_prediction[[0],[i]] = 1
        else: 
            Y_prediction[[0],[i]] = 0
    
    return Y_prediction




def signup_view(request):
    if request.user.is_authenticated:
        return redirect('service')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                username = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + username )
                return redirect('services')

        context = {'form':form}
        return render(request, 'signin.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('services')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('services')
            else:
                messages.info(request, "Username or password is incorrect")
        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')


def index (request):
    return render(request, 'index.html')

@login_required(login_url = 'login')
def service(request):
    if request.method == 'POST' and request.FILES['selectfile']:
        myfile = request.FILES['selectfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        uploaded_file_url = fs.url(filename)
        uploaded_file_url = uploaded_file_url.replace("%20"," ")
        test = str(BASE_DIR)+uploaded_file_url
        my_image = read_image(test).reshape(1, ROWS*COLS*CHANNELS).T
        my_predicted_image = predict(data["w"], data["b"], my_image)
        res = np.squeeze(my_predicted_image)
        if res == 0.0:
            ans = "The image you provided contains brain tumor"
        else:
            ans = "The image you provided does not contains brain tumor"


        return render(request, 'service.html' , context={'ans':ans})
    return render(request, 'service.html')



