from django.db import models
import uuid

from users.models import Profile

from django.db.models.deletion import CASCADE

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-vote_ratio','-vote_total','title']

    @property
    def getvotecount(self):
        reviews=self.review_set.all()
        upvote=reviews.filter(value='up').count()
        totalvote=reviews.count()
        
        ratio=(upvote/totalvote)*100

        self.vote_total=totalvote
        self.vote_ratio=ratio
        self.save()

    @property
    def reviewers(self):
        queryset=self.review_set.all().values_list('owner__id',flat=True)
        return queryset


    @property
    def imageurl(self):
        try:
            img=self.featured_image.url
        except:
            img=""
        return img
class Review(models.Model):
    Vote_Type=(
        ("up","up vote"),
        ("down","down vote")
    )
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=50,choices=Vote_Type)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    class Meta:
        unique_together=[['owner','project']]
    
    def __str__(self):
        return self.value



class Tag(models.Model):
    name=models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)   

    def __str__(self):
        return self.name
