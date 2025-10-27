from rest_framework.permissions import BasePermission

# improve this permission later
class IsAdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
    
