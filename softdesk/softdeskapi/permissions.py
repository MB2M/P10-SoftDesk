from rest_framework import permissions

from .models import Comment, Contributor, Issue, Project



class IsAuthorOrContributor(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if isinstance(obj, Project):
            project = obj
        elif isinstance(obj, Issue):
            project = obj.project
        elif isinstance(obj, Comment):
            project = obj.issue.project

        methods = permissions.SAFE_METHODS

        #Only author can add an contributor to a project
        if view.get_view_name() != 'Project User List':
            methods += ('POST',)

        if request.method in methods:
            return Contributor.objects.filter(user=request.user.id, project=project.id).exists()

        # Instance must have an attribute named `owner`.
        return obj.author == request.user

# class IsContributor(permissions.BasePermission):
#     """
#     Object-level permission to only allow contributors of an object to edit it.
#     Assumes the model instance has an `owner` attribute.
#     """

#     def has_object_permission(self, request, view, obj):
#         return Contributor.objects.filter(user=request.user).filter(project=obj).exists()
