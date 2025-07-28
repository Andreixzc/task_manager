# tasks/mutations.py
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Task
from categories.models import Category  # ← Fix: Import from categories, not tasks
from .types import TaskType

class CreateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        priority = graphene.String()
        category_id = graphene.Int()
        due_date = graphene.Date()
    
    task = graphene.Field(TaskType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, title, description="", priority="medium", category_id=None, due_date=None):
        try:
            # Get the user (in real app, you'd get from info.context.user)
            user = User.objects.first()  # For now, use first user
            if not user:
                return CreateTask(success=False, errors=["No user found"])
            
            # Get category if provided
            category = None
            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    return CreateTask(success=False, errors=["Category not found"])
            
            # Create the task
            task = Task.objects.create(
                title=title,
                description=description,
                priority=priority,
                category=category,
                due_date=due_date,
                created_by=user
            )
            
            return CreateTask(task=task, success=True, errors=[])
            
        except Exception as e:
            return CreateTask(success=False, errors=[str(e)])

class UpdateTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()
        priority = graphene.String()
        category_id = graphene.Int()
        due_date = graphene.Date()
    
    task = graphene.Field(TaskType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, task_id, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
            
            # Update fields if provided
            if 'title' in kwargs:
                task.title = kwargs['title']
            if 'description' in kwargs:
                task.description = kwargs['description']
            if 'completed' in kwargs:
                task.completed = kwargs['completed']
            if 'priority' in kwargs:
                task.priority = kwargs['priority']
            if 'due_date' in kwargs:
                task.due_date = kwargs['due_date']
            
            # Handle category update
            if 'category_id' in kwargs:
                if kwargs['category_id']:
                    try:
                        category = Category.objects.get(id=kwargs['category_id'])
                        task.category = category
                    except Category.DoesNotExist:
                        return UpdateTask(success=False, errors=["Category not found"])
                else:
                    task.category = None
            
            task.save()
            return UpdateTask(task=task, success=True, errors=[])
            
        except Task.DoesNotExist:
            return UpdateTask(success=False, errors=["Task not found"])
        except Exception as e:
            return UpdateTask(success=False, errors=[str(e)])

class DeleteTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.Int(required=True)
    
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, task_id):
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return DeleteTask(success=True, errors=[])
        except Task.DoesNotExist:
            return DeleteTask(success=False, errors=["Task not found"])
        except Exception as e:
            return DeleteTask(success=False, errors=[str(e)])

class TaskMutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()