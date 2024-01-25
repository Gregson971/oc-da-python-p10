from rest_framework import serializers

from .models import Project, Issue, Comment, Contributor


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']


class ProjectDetailSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time', 'issues', 'contributors']

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project_id=instance.id)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'assigned_to', 'priority', 'tag', 'status', 'project', 'author']


class IssueDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

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
            'comments',
        ]

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance.id)
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'uuid', 'author', 'issue', 'created_time']


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'uuid', 'author', 'issue', 'created_time']


class ContributorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'role', 'user', 'project', 'created_time']


class ContributorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'role', 'user', 'project', 'created_time']
