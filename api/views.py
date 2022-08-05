from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.managerserializer import IssueSerializer

from dropship.models import Issue


class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]
   

    def get(self, request):
        serializer = IssueSerializer(Issue.objects.all(), many=True)
        return JsonResponse(serializer.data)