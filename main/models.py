from django.db import models
from django.contrib.postgres.fields import JSONField
from users.models import Users

class Teams(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'
        verbose_name_plural = "Teams"

class Roles(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'
        verbose_name_plural = "Roles"

class TeamMembers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, db_column='team_id')
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, db_column='role_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'team_members'
        verbose_name_plural = "Team Members"

class Projects(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    data = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'
        verbose_name_plural = "Projects"

class TeamProjects(models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, db_column='team_id')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, db_column='project_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'team_projects'
        verbose_name_plural = "Team Projects"

class Sections(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, db_column='project_id')
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sections'
        verbose_name_plural = "Sections"

class Categories(models.Model):
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, db_column='section_id')
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = JSONField(default=[])

    class Meta:
        db_table = 'categories'
        verbose_name_plural = "Categories"

class Elements(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, db_column='category_id')
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = JSONField(default=[])

    class Meta:
        db_table = 'elements'
        verbose_name_plural = "Elements"

class Items(models.Model):
    element = models.ForeignKey(Elements, on_delete=models.CASCADE, db_column='element_id')
    type = models.CharField(max_length=100)
    content = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'items'
        verbose_name_plural = "Items"

class Comments(models.Model):
    element = models.ForeignKey(Elements, on_delete=models.CASCADE, db_column='element_id')
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, db_column='user_id')
    content = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        verbose_name_plural = "Comments"

class ProjectMembers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, db_column='project_id')
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, db_column='role_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_members'
        verbose_name_plural = "Project Members"