from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.utils.text import slugify
from django.db.models import Q, query

from realworld.models import Article, Tag
from .author_serializer import AuthorSerializer

class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(max_length=255, read_only=True)
    createdAt  = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt  = serializers.DateTimeField(source='updated_at', read_only=True)
    author = AuthorSerializer(read_only=True)
    tagList = serializers.PrimaryKeyRelatedField(
        source='tags',
        many=True,
        queryset = Tag.objects.all()
    )
    favorited = serializers.ReadOnlyField()
    favoritesCount = serializers.ReadOnlyField(source='favorites_count')

    class Meta:
        model = Article
        fields = ('slug', 'title', 'description', 'body', 'createdAt', 'updatedAt', 'author', 'tagList', 'favorited', 'favoritesCount')

    def validate_title(self, value):
        slug = slugify(value)
        q = Q(slug=slug)
        if self.instance:
            q &= ~Q(id=self.instance.id)

        if Article.objects.filter(q).exists():
            raise ValidationError('Article with same title already exist')
        return value

    def to_internal_value(self, data):
        resource_data = data['article']
        return super().to_internal_value(resource_data)

    def to_representation(self, instance):
        if isinstance(self.instance, query.QuerySet):
            return super().to_representation(instance)

        return {
            'article': super().to_representation(instance)
        }

    def run_validation(self, data=serializers.empty):

        if 'tagList' in data['article']:
            tagList = data['article']['tagList']
            for tag_name in tagList:
                tag, created = Tag.objects.get_or_create(name=tag_name)
        return super(ArticleSerializer, self).run_validation(data)

    def create(self, validated_data):
        current_user = self.context['request'].user
        tags = validated_data.pop('tags')

        obj = Article(**validated_data)
        obj.slug = slugify(validated_data['title'])
        obj.author = current_user
        obj.save()

        for tag in tags:
            obj.tags.add(tag)

        return obj

    def update(self, instance, validated_data):
        instance.slug = slugify(validated_data.get('title', instance.title))
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance