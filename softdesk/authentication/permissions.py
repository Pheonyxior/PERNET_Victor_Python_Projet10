from rest_framework import permissions


class UserViewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
    

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_staff or request.method in permissions.SAFE_METHODS:
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
