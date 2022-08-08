from dataclasses import fields
from rest_framework import serializers, viewsets, status
from dropship.models import Issue,Project

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