from django.contrib import admin
from main.models import *

class TeamsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'description', 'created_at', 'updated_at']
    class Meta:
        model = Teams

class RolesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'created_at', 'updated_at']
    class Meta:
        model = Roles

class TeamMembersAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'role__name', 'team__name']
    list_display = ['user', 'team', 'role', 'created_at', 'updated_at']
    class Meta:
        model = TeamMembers

class ProjectsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'description', 'created_at', 'updated_at']
    class Meta:
        model = Projects

class TeamProjectsAdmin(admin.ModelAdmin):
    search_fields = ['team__name', 'project__name']
    list_display = ['team', 'project', 'created_at', 'updated_at']
    class Meta:
        model = TeamProjects

class SectionsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'project__name']
    list_display = ['name', 'project', 'description', 'created_at', 'updated_at']
    class Meta:
        model = Sections

class CategoriesAdmin(admin.ModelAdmin):
    search_fields = ['name', 'section__name']
    list_display = ['name', 'section', 'description', 'created_at', 'updated_at']
    class Meta:
        model = Categories

class ElementsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'category__name']
    list_display = ['title', 'category', 'description', 'tags', 'created_at', 'updated_at']

    class Meta:
        model = Elements

class ItemsAdmin(admin.ModelAdmin):
    search_fields = ['element__title']
    list_display = ['element', 'content', 'created_at', 'updated_at']
    class Meta:
        model = Items

class CommentsAdmin(admin.ModelAdmin):
    search_fields = ['element__title', 'user__email']
    list_display = ['element', 'user', 'content', 'created_at', 'updated_at']
    class Meta:
        model = Comments

admin.site.register(Teams, TeamsAdmin)
admin.site.register(Roles, RolesAdmin)
admin.site.register(TeamMembers, TeamMembersAdmin)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(TeamProjects, TeamProjectsAdmin)
admin.site.register(Sections, SectionsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Elements, ElementsAdmin)
admin.site.register(Items, ItemsAdmin)
admin.site.register(Comments, CommentsAdmin)
