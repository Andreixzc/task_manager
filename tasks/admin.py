from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "priority",
        "completed",
        "due_date",
        "created_by",
    ]
    list_filter = ["completed", "priority", "category", "created_date"]
    search_fields = ["title", "description"]
    list_editable = ["completed"]
    date_hierarchy = "created_date"
