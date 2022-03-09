from django.shortcuts import render, redirect, render_to_response, reverse
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from login.models import Profile
from django.contrib import messages
from .forms import *
from django.template import RequestContext
from django.views.generic import DetailView

def index(request):
    #Get the model
    User = get_user_model()
    #Get the username from session data
    sess = request.session['sess']
    #Retrive the current user that matches the username
    #current = User.objects.get(username=sess)
    try:
        current = User.objects.get(username=sess)
    except Profile.DoesNotExist:
        current = Profile(user=request.user)
    form = AvaForm(request.POST, request.FILES)


    #POST request to update data from user:
    if "getInfo" in request.POST:
        displayName = request.POST['displayName']
        if displayName != '':
            current.first_name = displayName
    
        age = request.POST['age']
        if age != '':
            current.profile.age = age

        species = request.POST['species']
        if species != '':
            current.profile.species = species

        breed = request.POST['breed']
        if breed != '':
            current.profile.breed = breed

        gender = request.POST['gender']
        if gender != '':
            current.profile.gender = gender

        trait = request.POST['trait']
        if trait != '':
            current.profile.trait = trait

        location = request.POST['location']
        if location != '':
            current.profile.location = location

        bio = request.POST['bio']
        if bio != '':
            current.profile.bio = bio
        
        #Save update
        current.profile.save()
        current.save()
        return render(request, 'your_profile.html', {'form' : form})
        #return index(request)

    #Get all attributes and values and pass into a Dictionary
    #Use any of the following methods
    #Attrib = User.objects.filter(username=sess).values()[0]
    #Attrib = current.__dict__
    #Attrib = model_to_dict(current)

    #print(Attrib)
    elif "updateAva" in request.POST:
        if form.is_valid():
            current.profile.userAva = request.FILES["userAva"]
            current.profile.save()
            return render(request, 'your_profile.html', {'form' : form})
    else:
        UserInfo = current.get_short_name() + ":"
        UserInfo = UserInfo + str(current.profile.age) + ":"
        UserInfo = UserInfo + current.profile.species + ":"
        UserInfo = UserInfo + current.profile.breed + ":"
        UserInfo = UserInfo + current.profile.gender + ":"
        UserInfo = UserInfo + current.profile.trait + ":"
        UserInfo = UserInfo + current.profile.location + ":"
        UserInfo = UserInfo + current.profile.bio + ":"
        
        #Pass the user information through message
        messages.add_message(request, messages.INFO, UserInfo)

        #User does not have a profile pic
        if not current.profile.userAva:
            return render(request, 'your_profile.html', {'form' : form, 'path' : '/static/images/blankAva1.PNG'})    
        else:
            return render(request, 'your_profile.html', {'form' : form, 'path' : current.profile.userAva.url})
        #return render_to_response('your_profile.html', {'form' : form}, context)
