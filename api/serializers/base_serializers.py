from rest_framework import serializers

from api.models import User


class BaseSerializer(serializers.ModelSerializer):
    def get_current_user(self):
        request = self.context.get('request')
        return User.objects.get(pk=request.user.pk) if request else None
