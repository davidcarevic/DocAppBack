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
router.register('project-members', ProjectMembersViewSet, basename='project-member')
router.register('user-projects', UsersProjectViewSet, basename='user-projects')
router.register('project-sections', ProjectSectionsView, basename='project-sections')
router.register('section-categories', SectionCategoriesView, basename='section-categories')
router.register('category-elements', CategoryElementsView, basename='category-elements')
router.register('reorder-elements', ReorderElementsVeiwSet, basename='reorder-elements')
router.register('reorder-items', ReorderItemsVeiwSet, basename='reorder-items')
router.register('element-items', ElementItemsViewSet, basename='element-items')
