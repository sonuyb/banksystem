from rest_framework import permissions

class IsStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
            return  request.user.is_staff or request.user.is_superuser

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
            return  not(request.user.is_staff or request.user.is_superuser)
        
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
            return  request.user.is_superuser