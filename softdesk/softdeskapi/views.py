from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import mixins, status, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contributor, Project, User
from .serializers import ContributorSerializer, IssueSerializer, ProjectSerializer, UserSerializer
from .permissions import isAuthor, isContributor
from . import serializers


class ProjectList(generics.ListCreateAPIView):
    """
    List all projects of the users, or create a new project.
    """
    serializer_class = ProjectSerializer
    def get_queryset(self):
        return Project.objects.filter(users__id=self.request.user.id)

    def create(self, request):
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data._mutable = False
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.add_user(serializer.data['id'], role='author')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def add_user(self, project, role):
        data = {
            'project' : project,
            'role' : role,
            'user' : self.request.user.id,
            'permission' : 'create, read, update, delete',
        }
        serializer = ContributorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a project.
    """
    permission_classes = [isAuthor]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectUserList(generics.CreateAPIView, generics.RetrieveAPIView):
    """
    List all users of a project, or add a new user to the project.
    """
    permission_classes = [isAuthor]

    def get(self, request, pk):
        try:
            project = get_project(pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contributors = project.contributor_set.all()
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def post(self,request, pk, role='contributor'):
        self.request.data._mutable = True
        self.request.data['project'] = self.get_project(pk).id
        if role == 'contributor':
            self.request.data['permission'] = "create, read"
        else:
            self.request.data['permission'] = "create, read, update, delete"
        self.request.data['role'] = role
        self.request.data._mutable = False
        serializer = ContributorSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectUserDelete(generics.DestroyAPIView):
    """
    Delete a user from a project.
    """
    permission_classes = [isAuthor]

    def get_contributor(self, pk_project, pk_user):
        try:
            return Project.objects.get(pk=pk_project).contributor_set.filter(user=pk_user)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk_project, pk_user):
        contributor = self.get_contributor(pk_project, pk_user)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Signup(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

class IssueList(generics.ListCreateAPIView):
    """
    List all issues of a project, or add a new issue to the project.
    """
    permission_classes = [isAuthor, isContributor]
    serializers_class = IssueSerializer

    def get(self, request, pk):
        try:
            project = get_project(pk)
            self.check_object_permissions(self.request, project)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        issues = project.issue_set.all()
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def create(self, request):
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data['assignee'] = request.user.id
        request.data._mutable = False
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueDetail(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    Update or delete a project.
    """
    permission_classes = [isAuthor]
    serializer_class = IssueSerializer


@api_view(['GET', 'POST'])
def contributor_list(request):
    """
    List all contributors, or create a new contributor.
    """
    if request.method == 'GET':
        contributors = Contributor.objects.all()
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_project(pk):
        return Project.objects.get(pk=pk)

class UserList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()