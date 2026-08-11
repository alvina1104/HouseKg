from rest_framework.permissions import BasePermission

class CheckPropertyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'seller'

class CheckReviewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'buyer'