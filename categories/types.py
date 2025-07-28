# categories/types.py
import graphene
from graphene_django import DjangoObjectType
from .models import Category


class CategoryType(DjangoObjectType):
    task_count = graphene.Int()

    class Meta:
        model = Category
        fields = "__all__"

    def resolve_task_count(self, info):
        return self.task_set.count()
