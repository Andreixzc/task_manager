# taskmanager/schema.py
import graphene
from tasks.queries import TaskQuery
from tasks.mutations import TaskMutation
from categories.queries import CategoryQuery
from categories.mutations import CategoryMutation


class Query(TaskQuery, CategoryQuery, graphene.ObjectType):
    pass


class Mutation(TaskMutation, CategoryMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
