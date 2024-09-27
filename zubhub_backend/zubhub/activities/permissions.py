from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = "You must be the owner of this activity to perform this function"

    def has_object_permission(self, request, view, object):
        return object.creators.filter(id=request.user.pk).exists()


class IsStaffOrModeratorOrEducator(BasePermission):
    message = "You must be a staff a moderator or an educator to perform this function"

    def has_object_permission(self, request, view, object):
       
        return request.user.is_staff == True or request.user.tags.filter(name="moderator").exists() or request.user.tags.filter(name="educator").exists()
    
class IsStaffOrModerator(BasePermission):
    message = "You must be a staff a moderator to perform this function"

    def has_object_permission(self, request, view, object):
       
        return request.user.is_staff == True or request.user.tags.filter(name="moderator").exists()