from softdesk.models import User, Project, Issue, Comment
from rest_framework import serializers
from snippets.models import Snippet

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name="snippet-detail", read_only=True
    )

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["url", "id", "username", "password", "snippets"]
    
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    class Meta:
        model = Project
        fields = '__all__'


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    class Meta:
        model = Comment
        fields = '__all__'

