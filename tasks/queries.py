# tasks/queries.py
import graphene
from .models import Task
from .types import TaskType


class TaskQuery(graphene.ObjectType):
    # List all tasks
    tasks = graphene.List(TaskType)
    # Get single task by ID
    task = graphene.Field(TaskType, id=graphene.Int(required=True))

    # Filter tasks by completion status
    completed_tasks = graphene.List(TaskType)
    pending_tasks = graphene.List(TaskType)

    # Filter tasks by priority
    high_priority_tasks = graphene.List(TaskType)

    def resolve_tasks(self, info):
        return Task.objects.all()

    def resolve_task(self, info, id):
        try:
            return Task.objects.get(id=id)
        except Task.DoesNotExist:
            return None

    def resolve_completed_tasks(self, info):
        return Task.objects.filter(completed=True)

    def resolve_pending_tasks(self, info):
        return Task.objects.filter(completed=False)

    def resolve_high_priority_tasks(self, info):
        return Task.objects.filter(priority="high")
