import graphene
from wagtailkit.api.graphql import graphql_schema

from .queries import WarehouseQuery

graphql_schema.register_query(WarehouseQuery)