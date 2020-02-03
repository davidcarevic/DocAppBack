from main.api.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('teams', TeamsViewSet, basename='teams')
router.register('roles', RolesViewSet, basename='roles')
router.register('team-members', TeamMembersViewSet, basename='team-members')
router.register('projects', ProjectsViewSet, basename='projects')
router.register('team-projects', TeamProjectsViewSet, basename='team-projects')
router.register('sections', SectionsViewSet, basename='sections')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('elements', ElementsViewSet, basename='elements')
router.register('items', ItemsViewSet, basename='items')
router.register('comments', CommentsViewSet, basename='comments')
router.register('users-teams', UsersTeamsView, basename='users-teams')
