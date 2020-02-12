from django.contrib import admin
from users.models import Users
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_display = ['email', 'is_active', 'is_admin', 'is_staff']
    list_filter = ['is_admin', 'is_staff', 'is_active']

    class Meta:
        model = Users


admin.site.register(Users, UserAdmin)
admin.site.unregister(Group)
