from django.urls import path
from .views import SnippetListCreateView, SnippetDetailUpdateDestroyView, TagListView, TagDetailView


urlpatterns = [
    path('', SnippetListCreateView.as_view(), name='snippet-list-create'),
    path('<int:pk>/', SnippetDetailUpdateDestroyView.as_view(), name='snippet-detail-update-destroy'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag-detail')
]
