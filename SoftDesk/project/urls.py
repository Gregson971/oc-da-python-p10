from rest_framework_nested import routers

from .views import ProjectViewSet, IssueViewSet, CommentViewSet, ContributorViewSet

project_router = routers.SimpleRouter()
project_router.register("projects", ProjectViewSet, basename="projects")

issue_router = routers.NestedSimpleRouter(project_router, 'projects', lookup='projects')
issue_router.register("issues", IssueViewSet, basename="project-issues")

comment_router = routers.NestedSimpleRouter(issue_router, 'issues', lookup='issues')
comment_router.register("comments", CommentViewSet, basename="issue-comments")

contributor_router = routers.NestedSimpleRouter(project_router, 'projects', lookup='projects')
contributor_router.register("contributors", ContributorViewSet, basename="project-contributors")
