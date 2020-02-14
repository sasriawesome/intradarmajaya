from wagtailkit.api.graphql import graphql_schema

from .queries import ProductsQuery

graphql_schema.register_query(ProductsQuery)