from softdesk.models import User, Project, Issue, Comment, Contributor
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate(self, value):
        print(value)
        if value['age'] <= 15:
            raise serializers.ValidationError("You canno't create a SoftDesk account if you are under 15.")
        return value

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["url", "id", "username", "password", "age", "can_data_be_shared", "can_be_contacted"]

    
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    class Meta:
        model = Project
        fields = '__all__'


class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            allowed_projects = Contributor.objects.filter(user=request.user).values("project")
            self.fields["project"].queryset = Project.objects.filter(id__in=allowed_projects)
            allowed_users = Contributor.objects.filter(project__in=allowed_projects).values("user")
            queryset = User.objects.filter(id__in=allowed_users)
            self.fields["contributor_assigned"].queryset = queryset
    

    class Meta:
        model = Issue
        fields = '__all__'
        
    


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            allowed_projects = Contributor.objects.filter(user=request.user).values("project")
            self.fields["issue"].queryset = Issue.objects.filter(project__in=allowed_projects)
            

    class Meta:
        model = Comment
        fields = '__all__'

