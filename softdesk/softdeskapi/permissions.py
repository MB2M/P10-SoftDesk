from .models import Contributor
from rest_framework import permissions


class isAuthor(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user

class isContributor(permissions.BasePermission):
    """
    Object-level permission to only allow contributors of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        print("##############", Contributor.objects.filter(user=request.user).filter(project=obj).exists())
        # project_id = obj.project.id
        return Contributor.objects.filter(user=request.user).filter(project=obj).exists()
