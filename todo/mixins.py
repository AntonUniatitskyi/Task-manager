from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        # if instance.created_by != self.request.user and instance.executers != self.request.user:
        #     raise PermissionDenied
        if instance.created_by != self.request.user and not instance.executers.filter(executer_id=self.request.user.pk).exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
