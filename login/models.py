from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, blank=True)
    trait = models.CharField(max_length=50, blank=True)
    breed = models.TextField(max_length=50, blank=True)
    species = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    userAva = models.ImageField(upload_to='images', blank=True, null=True)
    #Them 2 truong nay
    whoLikeMe = models.TextField(default='', blank=True)
    matches = models.TextField(default='', blank=True)
    noInteract = models.TextField(default='', blank=True)
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#Chuc a yeu
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)

#@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
#def save_user_profile(sender, instance, created, **kwargs):
#    user = instance
#    if created:
#        profile = Profile(user=user)
#        profile.save()

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()

#@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
#def save_profile(sender, instance, created, **kwargs):
#    user = instance
#    if created:
#        profile = UserProfile(user=user)
#       profile.save()