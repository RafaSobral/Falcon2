from django.contrib import admin
from .models import Collaborator, Role

# Register your models here.

@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'role', 'contract', 'start_date', 'end_date')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('role', 'contract', 'start_date', 'end_date')
    ordering = ('start_date',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'description')
    search_fields = ('role', 'description')