from rest_framework import serializers
from .models import Snippet, Tag
from rest_framework.reverse import reverse


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']
    

class SnippetListSerializer(serializers.ModelSerializer):
    tag = serializers.CharField()
    detail = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'note', 'tag', 'created_at', 'updated_at', 'created_user', 'detail']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_user', 'detail']
    
    def get_detail(self, snippet):
        request = self.context.get('request')
        return reverse('snippet-detail-update-destroy', args=[snippet.pk], request=request)

    def create(self, validated_data):
        tag_title = validated_data.pop('tag')
        tag, _ = Tag.objects.get_or_create(title=tag_title)

        user = self.context['request'].user
        snippet = Snippet.objects.create(tag=tag, created_user=user, **validated_data)
        return snippet
    
    def to_representation(self, snippet):
        representation = super().to_representation(snippet)
        representation['tag'] = snippet.tag.title if snippet.tag else None
        representation['created_user'] = snippet.created_user.first_name + ' ' + snippet.created_user.last_name if snippet.created_user else None
        return representation
    

class SnippetDetailSerializer(serializers.ModelSerializer):
    tag = serializers.CharField()

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'note', 'tag', 'created_at', 'updated_at', 'created_user']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_user']
    
    def update(self, snippet, validated_data):
        tag_title = validated_data.pop('tag')
        tag, _ = Tag.objects.get_or_create(title=tag_title)
        snippet.tag = tag

        snippet.title = validated_data.get('title', snippet.title)
        snippet.note = validated_data.get('note', snippet.note)
        snippet.save()
        return snippet
    
    def to_representation(self, snippet):
        representation = super().to_representation(snippet)
        representation['tag'] = snippet.tag.title if snippet.tag else None
        representation['created_user'] = snippet.created_user.first_name + ' ' + snippet.created_user.last_name if snippet.created_user else None
        return representation
    

class TagListSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()
    class Meta:
        model = Tag
        fields = ['id', 'title', 'detail']

    def get_detail(self, tag):
        request = self.context.get('request')    
        return reverse('tag-detail', args=[tag.pk], request=request)
    

class TagDetailSerializer(serializers.ModelSerializer):
    snippets = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'title', 'snippets']

    def get_snippets(self, tag):
        request = self.context.get('request')
        snippets = Snippet.objects.filter(tag=tag, created_user=request.user)
        return SnippetListSerializer(snippets, many=True, context={'request': request}).data

