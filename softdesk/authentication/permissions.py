from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class ProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(view.action)
        if view.action == 'create':
            print(request.user, " is trying to create")
            return request.user.is_authenticated
        elif view.action == 'destroy':
            print(request.user, " is trying to destroy")
            return obj.owner == request.user
        print(request.user, " is trying to do some other action")
        return obj.contributors.filter(id=request.user.id).exists()


class IssuePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        elif view.action == 'create':
            if request.user.is_authenticated:
                is_contributor = obj

        return obj.owner == request.user