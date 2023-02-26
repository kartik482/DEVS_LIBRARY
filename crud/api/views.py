# from django.http import JsonResponse

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from .serializers import Projectserializer
from crudapp.models import Project,Review


@api_view(['GET'])
def getroutes(request):

    routes=[
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/user/token'},
        {'POST':'/api/user/token/refresh'},
        
    ]

    return Response(routes)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getprojects(request):
    # print('user:',request.user)
    projects=Project.objects.all()
    serializer=Projectserializer(projects,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getproject(request,pk):#get single project
    project=Project.objects.get(id=pk)
    serializer=Projectserializer(project,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectvote(request,pk):
    project=Project.objects.get(id=pk)
    user=request.user.profile
    data=request.data
    # print('data:',data)
    review,created=Review.objects.get_or_create(
        owner=user,
        project=project,

    )

    review.value=data['value']
    review.save()

    project.getvotecount ##getting property decorator from models
    serializer=Projectserializer(project,many=False)
    return Response(serializer.data)


