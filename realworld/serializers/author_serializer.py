from rest_framework import serializers

from realworld.models import CustomUser

class AuthorSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=1000, read_only=True)
    password = serializers.CharField(min_length=6, max_length=1000)

    class Meta:
        model = CustomUser
        fields = ('email', 'token', 'username', 'password', 'bio', 'image')

    def to_representation(self, instance):
        current_user = self.context['request'].user
        following = instance.following(current_user)

        return {
            **super().to_representation(instance),
            'following': following
        }