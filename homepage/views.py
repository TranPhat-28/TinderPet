from django.shortcuts import render, render_to_response
from django.contrib import messages
from importlib import import_module
from django.conf import settings
from login.models import *
from django.template import RequestContext
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import JsonResponse

def index(request):
    #Get the model
    User = get_user_model()
    #Get the username from session data
    sess = request.session['sess']

    #Retrieve urself
    yourSelf = User.objects.get(username=sess)
    tempString = yourSelf.profile.noInteract
    tempNointeractList = tempString.split(";")

    #Retrieve all users in db and store in a global var (Type: QuerySet)
    global users
    users = User.objects.all()

    #Make a list of all current username, except admin, lala, and currently loged-in user
    #And exclude the MATCHED user
    global userList
    userList = []
    global countNoInteract
    countNoInteract = tempString.count(';')
    for item in users:
        if item.username not in ('admin', 'lala', sess) and item.username not in tempNointeractList:
            if "--" not in item.username:
                userList.append(item.username)
            else:
                countNoInteract += 1
    
    #Get the username of the user will be display
    currentUsername = userList[0]
    #Retrive the current user that matches the username
    try:
        current = User.objects.get(username=currentUsername)
    except Profile.DoesNotExist:
        current = Profile(user=request.user)

    #Return first user
    data = {
            'nextUser': current.get_short_name(),
            'nextAge':(str(current.profile.age)),
            'nextSpecies':current.profile.species,
            'nextBreed':current.profile.breed,
            'nextGender':current.profile.gender,
            'nextTrait':current.profile.trait,
            'nextLocation':current.profile.location,
            'nextBio':current.profile.bio,
            'avaPath' : current.profile.userAva.url,
            'username':currentUsername
        }

    return render(request, 'homepage.html', data)

def queryNextUser(request):
    #Get the currentNo of user to retrieve information (sent from client)
    if "current" in request.GET:
        currentCount = int(request.GET["current"])

    #Number of current user (minus 3: admin, lala, currentUser)
    countMax = users.count() - 3 - countNoInteract

    #Check if out of range
    #If in range
    if currentCount < countMax:
        #Get the model
        User = get_user_model()
        #Get the username of the user will be display
        currentUsername = userList[currentCount]
        #Retrive the current user that matches the username
        try:
            current = User.objects.get(username=currentUsername)
        except Profile.DoesNotExist:
            current = Profile(user=request.user)
        #Retrive the desired information
        #print(currentUsername)
        
        if not current.profile.userAva:
            avaPath = '/static/images/blankAva1.PNG'
        else:
            avaPath = current.profile.userAva.url

        data = {
            'nextUser': current.get_short_name(),
            'nextAge':(str(current.profile.age)),
            'nextSpecies':current.profile.species,
            'nextBreed':current.profile.breed,
            'nextGender':current.profile.gender,
            'nextTrait':current.profile.trait,
            'nextLocation':current.profile.location,
            'nextBio':current.profile.bio,
            'avaPath':avaPath,
            'username':currentUsername
        }
    else:
        data = {
            'nextUser': '',
        }
    print("NOPE")
    return JsonResponse(data)

def likeAndQueryNext(request):
#Query the next user to display
    #Get the currentNo of user to retrieve information (sent from client)
    if "current" in request.GET:
        currentCount = int(request.GET["current"])

    #Number of current user (minus 3: admin, lala, currentUser)
    countMax = users.count() - 3

    #Check if out of range
    #If in range
    if currentCount < countMax:
        #Get the model
        User = get_user_model()
        #Get the username of the user will be display
        currentUsername = userList[currentCount]
        #Retrive the current user that matches the username
        try:
            current = User.objects.get(username=currentUsername)
        except Profile.DoesNotExist:
            current = Profile(user=request.user)
        #Retrive the desired information
        #print(currentUsername)
        
        if not current.profile.userAva:
            avaPath = '/static/images/blankAva1.PNG'
        else:
            avaPath = current.profile.userAva.url

        data = {
            'nextUser': current.get_short_name(),
            'nextAge':(str(current.profile.age)),
            'nextSpecies':current.profile.species,
            'nextBreed':current.profile.breed,
            'nextGender':current.profile.gender,
            'nextTrait':current.profile.trait,
            'nextLocation':current.profile.location,
            'nextBio':current.profile.bio,
            'avaPath':avaPath,
            'username':currentUsername
        }
    else:
        data = {
            'nextUser': '',
        }

#Handle the SEND LIKE
    #Liked username
    likedUsername = request.GET["liked"]
    #Current username from session data
    sess = request.session['sess']
    #If user liked = "empty" then do nothing, else add to that user whoLikeMe list
    if likedUsername != 'empty':
        print(sess + " sent a like to " + likedUsername)
        
        #Get the model
        User = get_user_model()
        #Retrive the liked user
        try:
            sendLike = User.objects.get(username=likedUsername)
        except Profile.DoesNotExist:
            sendLike = Profile(user=request.user)
        tempString = sendLike.profile.whoLikeMe
        #Check if already sent an like
        tempSplit = tempString.split(';')

        check = True
        for item in tempSplit:
            if item == sess:
                check = False
        #Chua like nguoi dung, duoc phep gui like den
        if check:
            #Nguoi dung da gui like cho minh, thuc hien match
            yourSelf = User.objects.get(username=sess)
            likeString = yourSelf.profile.whoLikeMe
            likeList = likeString.split(";")
            if sendLike.username in likeList:
                print("It's a match!")
                #Xoa user ra khoi danh sach ai like minh
                #print("Current whoLikeMe: " + likeString)
                removeThis = sendLike.username + ";"
                #print("User to remove: " + removeThis)
                newLikeString = likeString.replace(removeThis, "")
                #print("New whoLikeMe: " + newLikeString)
                yourSelf.profile.whoLikeMe = newLikeString
                #Add vao noInteract cho ca 2 user
                yourSelf.profile.noInteract += removeThis
                
                forThem = yourSelf.username + ';'
                sendLike.profile.noInteract += forThem
                #Them Key vao matches
                matchKey = yourSelf.username + "--" + sendLike.username + ";"
                yourSelf.profile.matches += matchKey
                sendLike.profile.matches += matchKey
                #Luu lai nhung thay doi cho ca 2 ben
                yourSelf.profile.save()
                sendLike.profile.save()
                #Create a user with username = keymatch just to store private messages
                email = "dataModel"
                username = matchKey[:-1]
                password1 = "dataModel"
                User.objects.create_user(username=username, email=email, password=password1)
                #Gui message
                data.update({"match": "yes"})
                print(data)
            #Nguoi dung chua gui like cho minh, thuc hien gui like den nguoi dung truoc
            else:
                print("Like ngta!")
                tempString += str(sess + ";")
                sendLike.profile.whoLikeMe = tempString
                sendLike.profile.save()
        #Da like nguoi dung, khong gui like trung lap nua
        #DO NOT SEND DUPLICATED LIKES
        else:
            print("Already liked")
    return JsonResponse(data)