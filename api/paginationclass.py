from rest_framework.pagination import LimitOffsetPagination

class custompaginate(LimitOffsetPagination):
    default_limit=3
    