from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Message, Profile,Skill
from users import models



class customusercreationform(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','email','username','password1','password2']
        labels={
            "first_name":"Name"
        }

    def __init__(self,*args,**kwargs):
        super(customusercreationform,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class profileForm(ModelForm):
    class Meta:
        model=Profile
        fields="__all__"
        exclude=["user"]

    def __init__(self,*args,**kwargs):
        super(profileForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class skillform(ModelForm):
    class Meta:
        model=Skill
        fields="__all__"
        exclude=["owner"]

    def __init__(self,*args,**kwargs):
        super(skillform,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class Messageform(ModelForm):
    class Meta:
        model=Message
        fields=['name','email','subject','body']

    def __init__(self,*args,**kwargs):
        super(Messageform,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        

