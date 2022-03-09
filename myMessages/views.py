from re import match
from django.shortcuts import render
from django.contrib import messages
from importlib import import_module
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def index(request):
    #Get the model
    User = get_user_model()
    #Get the username from session data
    sess = request.session['sess']
    #Retrieve urself
    yourSelf = User.objects.get(username=sess)
    matches = yourSelf.profile.matches
    returnString = matches[:-1]

    displayNameString = returnString.replace(sess, '')
    displayNameString1 = displayNameString.replace('--', '')
    returnDisplayNameString = ''
    tempList = displayNameString1.split(';')
    for item in tempList:
        tempUser = User.objects.get(username=item)
        returnDisplayNameString = returnDisplayNameString + tempUser.get_short_name() + ';'
    #print(returnDisplayNameString)
    returnDisplayNameString1 = returnDisplayNameString[:-1]
    
    return render(request, 'myMessages.html', {'matchKeys': returnString, 'displayName': returnDisplayNameString1})

def updateMessage(request):
    #Get the model
    User = get_user_model()
    #Get the username from session data
    sess = request.session['sess']
    #Retrieve urself
    yourSelf = User.objects.get(username=sess)

    #MatchKey
    matchKey = request.GET['matchKey']
    #Message
    msg = '--[[[' + yourSelf.get_short_name() + ']]]--' + request.GET['msg'] + ';'
    
    #Retrieve the dataModel
    dataModel = User.objects.get(username=matchKey)
    dataModel.profile.noInteract += msg
    dataModel.profile.save()

    return JsonResponse({'key' : 'value'})

def fetchAll(request):
    matchKey = request.GET['matchKey']
    #print("Fetch from this: " + matchKey)
    #Get the model
    User = get_user_model()
    #Retrieve the dataModel
    dataModel = User.objects.get(username=matchKey)
    dataStringtmp = dataModel.profile.noInteract
    dataString = dataStringtmp[:-1]

    #Your Display name
    yourself = User.objects.get(username=request.session['sess'])
    yourName = yourself.get_short_name()
    #Their Display name
    tmp1 = matchKey.replace(request.session['sess'], '')
    tmp2 = tmp1.replace('--', '')
    themself = User.objects.get(username=tmp2)
    themName = themself.get_short_name()
    return JsonResponse({'dataString' : dataString, 'yourName' : yourName, 'theirName' : themName})