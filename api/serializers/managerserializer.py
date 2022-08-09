from dataclasses import fields
from pyexpat import model

from rest_framework import serializers, viewsets, status
from dropship.models import CommentIssue, Issue, Label,Project

class IssueSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Issue
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model=Project
        fields = '__all__'

class IssueAssign(serializers.ModelSerializer):
     class Meta:
        model=Issue
        fields = ('assigned',)

class IssueStatus(serializers.ModelSerializer):
     class Meta:
        model=Issue
        fields = ('status')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentIssue
        fields = '__all__'

class LableSerializer(serializers.ModelSerializer):
    class Meta:
        model=Label
        fields='__all__'