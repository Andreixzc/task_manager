# tasks/types.py
import graphene
from graphene_django import DjangoObjectType
from .models import Task


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"
