# categories/queries.py
import graphene
from .models import Category
from .types import CategoryType


class CategoryQuery(graphene.ObjectType):
    # List all categories
    categories = graphene.List(CategoryType)
    # Get single category by ID
    category = graphene.Field(CategoryType, id=graphene.Int(required=True))

    # Custom queries
    categories_with_tasks = graphene.List(CategoryType)
    empty_categories = graphene.List(CategoryType)

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_category(self, info, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def resolve_categories_with_tasks(self, info):
        return Category.objects.filter(task__isnull=False).distinct()

    def resolve_empty_categories(self, info):
        return Category.objects.filter(task__isnull=True)
