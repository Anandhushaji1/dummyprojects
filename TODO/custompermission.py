from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    message="you have no permission to delete"
      
    def has_object_permission(self, request, view, obj):

        return obj.user == request.user 