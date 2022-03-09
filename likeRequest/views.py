from django.shortcuts import render
from django.contrib.auth.models import User
from login.models import Profile
from django.contrib.auth import get_user_model

# Create your views here.
def index(request):
    #Get the model
    User = get_user_model()
    #Get the username from session data
    sess = request.session['sess']
    #Retrive the current user that matches the username
    try:
        current = User.objects.get(username=sess)
    except Profile.DoesNotExist:
        current = Profile(user=request.user)

    #Dict to return
    returnDict = {}

    #String of whoLikeMe
    stringData = current.profile.whoLikeMe
    if stringData != '':
        stringData = stringData[:-1]
        likeList = stringData.split(';')
        returnDict.update({"likeCount" : len(likeList)})
        tempProfileData = ""
        for item in likeList:
            #Handle each user info
            #Retrive the current user that matches the username        
            #try:
            tempProfile = User.objects.get(username=item)
            #except Profile.DoesNotExist:
            #    tempProfile = Profile(user=request.user)

            tempProfileData = tempProfileData + tempProfile.get_short_name() + ";"
            tempProfileData = tempProfileData + str(tempProfile.profile.age) + ";"
            tempProfileData = tempProfileData + tempProfile.profile.species + ";"
            tempProfileData = tempProfileData + tempProfile.profile.breed + ";"
            tempProfileData = tempProfileData + tempProfile.profile.gender + ";"
            tempProfileData = tempProfileData + tempProfile.profile.trait + ";"
            tempProfileData = tempProfileData + tempProfile.profile.location + ";"
            tempProfileData = tempProfileData + tempProfile.profile.bio + ";"
            #print(tempProfileData)
            if not tempProfile.profile.userAva:
                tempProfileData = tempProfileData + "noAvaPath" + "---"
            else:
                tempProfileData = tempProfileData + tempProfile.profile.userAva.url + "---"
        returnDict.update({"data" : tempProfileData})
    else:
        returnDict.update({"likeCount" : "0"})
    #Return result to template
    print(returnDict)
    return render(request, 'like_request.html', returnDict)
