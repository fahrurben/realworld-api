from rest_framework import serializers
from django.db.models import Q, query

from realworld.models import Comment, Article
from .author_serializer import AuthorSerializer

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    author = AuthorSerializer(read_only=True, context={'request'})

    class Meta:
        model = Comment
        fields = ('id', 'body', 'createdAt', 'updatedAt', 'author')

    def to_internal_value(self, data):
        resource_data = data['comment']
        return super().to_internal_value(resource_data)

    def to_representation(self, instance):
        if isinstance(self.instance, query.QuerySet):
            return super().to_representation(instance)

        return {
            'comment': super().to_representation(instance)
        }

    def create(self, validated_data):
        current_user = self.context['request'].user
        article_id = self.context['article_id']

        article = Article.objects.get(pk=article_id)

        obj = Comment(**validated_data)
        obj.article = article
        obj.author = current_user
        obj.save()

        return obj

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance
