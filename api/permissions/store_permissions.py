from rest_framework import permissions

from api.models import StoreStaff


def get_store_id_from_request(request, view, obj=None):
    store_id = view.kwargs.get('store_id')
    if store_id is not None:
        return store_id
    return None


class IsStoreOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user is None or request.user.is_anonymous():
            return False

        store_id = get_store_id_from_request(request, view)
        store_staff = StoreStaff.objects.filter(user=request.user, store__pk=store_id).get()
        return bool(store_staff is not None and store_staff.is_active)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)