from rest_framework.permissions import BasePermission

class IsStaff(BasePermission):
    """
    Permission class to allow access only to authenticated staff users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class CustomPermission(BasePermission):
    """
    Custom permission to allow POST requests only for admin users
    and GET requests only for staff users.
    """

    def has_permission(self, request, view):
        if request.method in ['POST','PUT', 'PATCH', 'DELETE']:
            # allow PUT, PATCH, DELETE requests for admin users
            return request.user.is_authenticated and request.user.is_superuser
        elif request.method == 'GET':
            # allow GET requests for staff users
            return request.user.is_authenticated and request.user.is_staff
        return False