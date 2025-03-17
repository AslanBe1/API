from datetime import timedelta, datetime
from django.utils import timezone
from rest_framework.permissions import BasePermission
from api.models import Product


class GetOrPostPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET','POST','PUT','DELETE']:
            return True
        return False


class DeleteTimePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Product):
            if request.method == "DELETE":
                time_difference = timezone.now() - obj.created_at
                return time_difference < timedelta(minutes=1)
        return True


class IsWorkListPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET','POST','PUT','DELETE']:
            return datetime.today().weekday() in range(0,5)
