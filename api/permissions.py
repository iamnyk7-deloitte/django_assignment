from typing import Type

from django.http.request import HttpRequest
from requests import request
from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    

    def has_permission(self, request: Type[HttpRequest], view):
        if request.user.is_manager:
            return bool(request.user and request.user.is_manager and request.user.is_authenticated)
        return False