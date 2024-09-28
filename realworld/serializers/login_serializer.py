from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)

    def to_internal_value(self, data):
        resource_data = data['user']
        return super().to_internal_value(resource_data)