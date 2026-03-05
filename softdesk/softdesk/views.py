from rest_framework import permissions, viewsets, generics
from django.db.models import Q

from softdesk.models import User, Project, Issue, Comment, Contributor
from softdesk.serializers import (
    UserSerializer, ProjectSerializer, IssueSerializer, CommentSerializer, 
    ContributorSerializer)
from authentication.permissions import UserViewPermission, IsAuthorOrReadOnly, IsContributor, IsUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    permission_classes = [
        UserViewPermission,
        ]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("time_created")
    serializer_class = ProjectSerializer
    contributor_serializer = ContributorSerializer
    permission_classes = [ 
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
        IsContributor
        ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all().order_by('-id')
    serializer_class = ContributorSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsContributor,
        IsUser,
        ]

    def get_queryset(self):
            # Prendre les projets auquel notre utilisateur contribue
            # Filtrer tout les contributeurs si leurs projets figurent dans la liste de projets
        if not self.request.user.is_authenticated:
            return Contributor.objects.none()
        user_projects = Contributor.objects.filter(user=self.request.user).values("project")
        my_filter_qs = Q()
        my_filter_qs = my_filter_qs | Q(project__in=user_projects)
        return Contributor.objects.filter(my_filter_qs)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
        IsContributor
        ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, 
                        contributor_assigned=self.request.user)
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Issue.objects.none()
        user_projects = Contributor.objects.filter(user=self.request.user).values_list("project", flat=True)
        my_filter_qs = Q()
        my_filter_qs = my_filter_qs | Q(project__in=user_projects)
        return Issue.objects.filter(my_filter_qs).order_by("time_created")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
        IsContributor
        ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Comment.objects.none()
        user_projects = Contributor.objects.filter(user=self.request.user).values("project")
        my_filter_qs = Q()
        my_filter_qs = my_filter_qs | Q(issue__project__in=user_projects)
        return Comment.objects.filter(my_filter_qs).order_by("time_created")
    