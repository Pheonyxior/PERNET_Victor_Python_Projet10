from rest_framework import permissions
from operator import attrgetter


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the snippet.
        return obj.author == request.user


class IsContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if getattr(obj, "contributors", None):
            return obj.contributors.filter(id=request.user.id).exists()
        elif getattr(obj, "project", None):
            return obj.project.contributors.filter(id=request.user.id).exists()
        elif getattr(obj, "issue", None):
            return obj.issue.project.contributors.filter(id=request.user.id).exists()
        else:
            return False

class ProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(view.action)
        if view.action == 'create':
            print(request.user, " is trying to create")
            return request.user.is_authenticated
        elif view.action == 'destroy':
            print(request.user, " is trying to destroy")
            return obj.author == request.user
        print(request.user, " is trying to do some other action")
        return obj.contributors.filter(id=request.user.id).exists()


class IssuePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        elif view.action == 'create':
            if request.user.is_authenticated:
                is_contributor = obj

        return obj.author == request.user