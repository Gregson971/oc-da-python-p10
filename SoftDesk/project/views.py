from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import Q

from .models import Project, Issue, Comment, Contributor

from .permissions import IsAdminAuthenticated

from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    ContributorListSerializer,
    ContributorDetailSerializer,
)


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()


class IssueViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])


class CommentViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])


class ContributorViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])
