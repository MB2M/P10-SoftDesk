from django.shortcuts import redirect, render
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Comment, Contributor, Issue, Project, User
from .serializers import CommentSerializer, ContributorSerializer, IssueSerializer, ProjectSerializer, ProjectUpdateSerializer, UserSerializer
from .permissions import IsAuthorOrContributor


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
    permission_classes = [IsAuthorOrContributor]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def put(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data._mutable = False
        return self.update(request, *args, **kwargs)

class ProjectUserList(generics.ListCreateAPIView):
    """
    List all users of a project, or add a new user to the project.
    """
    permission_classes = [IsAuthorOrContributor]
    serializer_class = ContributorSerializer
    queryset = Project.objects.all()

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contributors = project.contributor_set.all()
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def post(self,request, pk, role='contributor'):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.request.data._mutable = True
        self.request.data['project'] = project.id
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
    permission_classes = [IsAuthorOrContributor]

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
    permission_classes = [IsAuthorOrContributor]
    serializer_class = IssueSerializer

    def get_queryset(self):
        project_id = self.kwargs['pk']
        project = generics.get_object_or_404(Project, pk=project_id)
        self.check_object_permissions(self.request, project)
        return project.issue_set.all()

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs['pk']
        project = generics.get_object_or_404(Project, pk=project_id)
        self.check_object_permissions(self.request, project)
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data['assignee'] = request.user.id
        request.data['project'] = project_id
        request.data._mutable = False
        return self.create(request, *args, **kwargs)

class IssueDetail(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    Update or delete an issue.
    """
    permission_classes = [IsAuthorOrContributor]
    serializer_class = IssueSerializer
    lookup_url_kwarg = 'pk_issue'
    queryset = Issue.objects.all()

    def put(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data['project'] = kwargs['pk_project']
        request.data._mutable = False
        return self.update(request, *args, **kwargs)

class CommentList(generics.ListCreateAPIView):
    """
    List all comments of a issue, or add a new comment to the issue.
    """
    permission_classes = [IsAuthorOrContributor]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        issue_id = self.kwargs['pk_issue']
        issue = generics.get_object_or_404(Issue, pk=issue_id)
        self.check_object_permissions(self.request, issue)
        return issue.comment_set.all()

    def post(self, request, *args, **kwargs):
        issue_id = self.kwargs['pk_issue']
        issue = generics.get_object_or_404(Issue, pk=issue_id)
        self.check_object_permissions(self.request, issue)
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data['issue'] = issue_id
        request.data._mutable = False
        return self.create(request, *args, **kwargs)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment.
    """
    permission_classes = [IsAuthorOrContributor]
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'pk_comment'
    queryset = Comment.objects.all()

    def put(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data['issue'] = kwargs['pk_issue']
        request.data._mutable = False
        return self.update(request, *args, **kwargs)

# class UserList(generics.ListAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()