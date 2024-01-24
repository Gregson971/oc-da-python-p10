from rest_framework import serializers

from .models import Project, Issue, Comment, Contributor


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']


class ProjectDetailSerializer(serializers.ModelSerializer):
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time', 'contributors']

    def get_contributors(self, instance):
        queryset = instance.contributors
        serializer = ContributorDetailSerializer(queryset, many=True)
        return serializer.data


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'assigned_to', 'priority', 'tag', 'status', 'project', 'author']


class IssueDetailSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'assigned_to',
            'priority',
            'tag',
            'status',
            'author',
            'project',
        ]

    def get_project(self, instance):
        queryset = instance.project
        serializer = ProjectDetailSerializer(queryset, many=True)
        return serializer.data


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'uuid', 'author', 'issue', 'created_time']


class CommentDetailSerializer(serializers.ModelSerializer):
    issue = IssueListSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'uuid', 'author', 'issue', 'created_time']

    def get_issue(self, instance):
        queryset = instance.issue
        serializer = IssueDetailSerializer(queryset, many=True)
        return serializer.data


class ContributorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'role', 'created_time']


class ContributorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'role', 'created_time']