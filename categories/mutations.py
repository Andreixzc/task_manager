# categories/mutations.py
import graphene
from .models import Category
from .types import CategoryType


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        color = graphene.String()

    category = graphene.Field(CategoryType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, name, description="", color="#007bff"):
        try:
            category = Category.objects.create(
                name=name, description=description, color=color
            )
            return CreateCategory(category=category, success=True, errors=[])
        except Exception as e:
            return CreateCategory(success=False, errors=[str(e)])


class UpdateCategory(graphene.Mutation):
    class Arguments:
        category_id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()
        color = graphene.String()

    category = graphene.Field(CategoryType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, category_id, **kwargs):
        try:
            category = Category.objects.get(id=category_id)

            if "name" in kwargs:
                category.name = kwargs["name"]
            if "description" in kwargs:
                category.description = kwargs["description"]
            if "color" in kwargs:
                category.color = kwargs["color"]

            category.save()
            return UpdateCategory(category=category, success=True, errors=[])

        except Category.DoesNotExist:
            return UpdateCategory(success=False, errors=["Category not found"])
        except Exception as e:
            return UpdateCategory(success=False, errors=[str(e)])


class DeleteCategory(graphene.Mutation):
    class Arguments:
        category_id = graphene.Int(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return DeleteCategory(success=True, errors=[])
        except Category.DoesNotExist:
            return DeleteCategory(success=False, errors=["Category not found"])
        except Exception as e:
            return DeleteCategory(success=False, errors=[str(e)])


class CategoryMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
