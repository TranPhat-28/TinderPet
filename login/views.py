from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from login.forms import RegistrationForm
from django.contrib import messages

# I dont know, backup i guess? Only return login.html
def indexBackup(request):
    return render(request, 'login.html')

def index(request):
    form = RegistrationForm()
    #Signup a new user
    if 'inputSignup' in request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Sign up successfully!')
            return render(request, 'login.html', {'form': form})
    #Login
    elif 'inputLogin' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        #Login success will redirect to homepage
        if user is not None:
            request.session['sess'] = username
            return redirect("homepage/")
        #Login fail
        else:
            messages.add_message(request, messages.INFO, 'Wrong Username or Password!')
            return render(request, 'login.html', {'form': form})
    else:
    #    messages.add_message(request, messages.INFO, 'FAIL2')
        return render(request, 'login.html', {'form': form})
    #return render(request, 'login.html', {'form': form})
