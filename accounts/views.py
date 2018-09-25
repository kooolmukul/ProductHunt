from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        # user clicked after entering info
        if request.POST['password'] == request.POST['confirmPassword']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'account/signup.html', {'error': 'Username already Exists!'})
            except:
                user = User.objects.create_user(username = request.POST['username'], password=request.POST['password'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'account/signup.html', {'error': 'Password dont match!'})                    
    else:
        return render(request, 'account/signup.html')


def signin(request):
    if request.method == 'POST':
        # user clicked after entering info
        user = auth.authenticate(username= request.POST['username'], password= request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'account/signin.html', {'error': 'Username OR password is incorrect!'})        
    else:    
        return render(request, 'account/signin.html')


def logout(request):
    # if request.method == 'POST':
    #     auth.logout(request)
    #     return redirect('home')
    auth.logout(request)
    return redirect('home')

    return render(request, 'account/signin.html')
