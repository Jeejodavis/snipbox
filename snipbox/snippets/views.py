from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Snippet, Tag
from .serializers import SnippetListSerializer, SnippetDetailSerializer, TagListSerializer, TagDetailSerializer
from rest_framework.response import Response

class IsUserCreatedSnippet(permissions.BasePermission):

    def has_object_permission(self, request, view, snippet):
        return snippet.created_user == request.user

class SnippetListCreateView(generics.ListCreateAPIView):
    serializer_class = SnippetListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Snippet.objects.filter(created_user=self.request.user).select_related('tag', 'created_user')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'total': queryset.count(),
            'data': serializer.data
        })

    def perform_create(self, serializer):
        serializer.save()
    
class SnippetDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SnippetDetailSerializer
    queryset = Snippet.objects.all().select_related('tag', 'created_user')
    permission_classes = [permissions.IsAuthenticated, IsUserCreatedSnippet]

    def delete(self, request, *args, **kwargs):
        snippet = self.get_object()
        self.perform_destroy(snippet)

        snippets = Snippet.objects.filter(created_user=self.request.user).select_related('tag', 'created_user')
        serializer = self.get_serializer(snippets, many=True, context={'request': request})
        return Response({
            'total': snippets.count(),
            'data': serializer.data
        })


class TagListView(generics.ListAPIView):
    serializer_class = TagListSerializer
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class TagDetailView(generics.RetrieveAPIView):
    serializer_class = TagDetailSerializer
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    