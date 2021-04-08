from django.db.models import fields
from rest_framework import serializers
from .models import Comment, Contributor, Issue, Project, User
from . import models


class ProjectSerializer(serializers.ModelSerializer):
    # users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author =  serializers.PrimaryKeyRelatedField(many=False,  queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author']

class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ContributorSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # project = ProjectSerializer()
    class Meta:
        model = Contributor
        fields = ['user', 'project', 'permission', 'role']

class IssueSerializer(serializers.ModelSerializer):
    # author =  serializers.PrimaryKeyRelatedField(many=False,  queryset=User.objects.all())

    class Meta:
        model = Issue
        fields = ['title', 'description', 'tag', 'priority', 'project', 'status', 'author', 'assignee', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description', 'author', 'issue', 'created_time']
        extra_kwargs = {'created_time': {'read_only': True}}