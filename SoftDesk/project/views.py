from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from authentication.models import User

from .models import Project, Issue, Comment, Contributor

from .permissions import ProjectPermission, IssuePermission, CommentPermission, ContributorPermission

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


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    permission_classes = [ProjectPermission]
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        projects_ids = [
            contributor.project_id for contributor in Contributor.objects.filter(user_id=self.request.user).all()
        ]
        return Project.objects.filter(id__in=projects_ids)

    @transaction.atomic
    def create(self, request):
        request.data['author'] = request.user.pk

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        project = Project.objects.get(pk=serializer.data['id'])
        Contributor.objects.create(user=request.user, project=project, role='CONTRIBUTOR')

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request.data['author'] = request.user.pk
        request.data['contributors'] = request.user.pk
        return super().update(request, *args, **kwargs)


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    permission_classes = [IssuePermission]
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['projects_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        print(request.user)
        request.data['author'] = request.user.pk
        request.data['project'] = self.kwargs['projects_pk']

        project = Project.objects.get(pk=self.kwargs['projects_pk'])
        assignee = User.objects.get(pk=request.data['assigned_to'])

        if assignee not in project.contributors.all():
            Contributor.objects.create(user=assignee, project=project, role='CONTRIBUTOR')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request.data['author'] = request.user.pk
        request.data['project'] = self.kwargs['projects_pk']
        return super().update(request, *args, **kwargs)


class CommentViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issues_pk'])


class ContributorViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['projects_pk'])
