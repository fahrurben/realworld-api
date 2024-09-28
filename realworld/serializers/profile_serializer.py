from rest_framework import serializers

from realworld.models import CustomUser

class ProfileSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=1000, read_only=True)
    password = serializers.CharField(min_length=6, max_length=1000)

    class Meta:
        model = CustomUser
        fields = ('email', 'token', 'username', 'password', 'bio', 'image')

    def to_internal_value(self, data):
        resource_data = data['profile']
        return super().to_internal_value(resource_data)

    def to_representation(self, instance):
        return {
            'profile': {
                'email': instance.email,
                'username': instance.username,
                'bio': instance.bio,
                'image': instance.image,
            }
        }