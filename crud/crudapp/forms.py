from dataclasses import fields
from pyexpat import model
from turtle import title
from django.forms import ModelForm
from django import forms

from .models import Project,Review

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields="__all__"
        exclude=["vote_total","vote_ratio","owner",'tags']
        widgets={
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)

        for key,value in self.fields.items():
            value.widget.attrs.update({'class':'input'})
            




        # self.fields["<enter a single field only use for loop to access all fields>"].widget.attrs.update({'class':'input'})


class Reviewform(ModelForm):
    class Meta:
        model=Review
        fields=['value','body']

        labels={
            'value' : 'Place your vote',
            'body' : 'Enter your comment '
        }
    def __init__(self,*args,**kwargs):
        super(Reviewform,self).__init__(*args,**kwargs)

        for key,value in self.fields.items():
            value.widget.attrs.update({'class':'input'})
            