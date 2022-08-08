from rest_framework import serializers, viewsets, status
from dropship.models import Issue

class IssueSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Issue
        fields = '__all__'