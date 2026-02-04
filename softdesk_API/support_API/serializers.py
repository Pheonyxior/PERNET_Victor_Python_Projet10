from support_API.models import Project, Issue, Comment

from rest_framework import serializers


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

