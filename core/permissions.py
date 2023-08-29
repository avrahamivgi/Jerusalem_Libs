from rest_framework.permissions import BasePermission
 
class IsCustomer(BasePermission):
    def has_permission(self, request , view):
        return request.user.groups.filter(name='library_customer').exists()

class IsLibraryWorker(BasePermission):
    def has_permission(self, request,view):
        return request.user.groups.filter(name='library_worker').exists()

class IsLibraryManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='library_manager').exists()