
from email import message
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete #for signalS
from django.dispatch import receiver
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings



# @receiver(post_save,sender=Profile)
def createprofile(sender,instance,created,**kwargs):
    if created:
        user=instance
        # profile=<class name>.objects.create(args of class) or
        Profile.objects.create( 
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name

        )

        #for sending email
        
        # subject='welcome to devsearch'
        # message='we are glad you are here '
        
        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [Profile.email],
        #     fail_silently=False
        # )



def updateprofile(sender,instance,created,**kwargs):
    profile=instance
    user=profile.user
    if created==False:
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()
        






# @receiver(post_delete,sender=Profile)
def deleteprofile(sender,instance,**kwargs):
    try:    
        user=instance.user
        user.delete()
    except:
        pass

post_save.connect(createprofile,sender=User)
post_delete.connect(deleteprofile,sender=Profile)
post_save.connect(updateprofile,sender=Profile)