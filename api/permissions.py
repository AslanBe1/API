import time
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.permissions import BasePermission

class GetOrPostPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET','POST','PUT','DELETE']:
            return True
        return False


class UpdateTimePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
            return (now() - obj.created_at) < timedelta(minutes=1)
