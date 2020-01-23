from wagtailkit.api.graphql import graphql_schema

from .queries import PersonQuery

graphql_schema.register_query(PersonQuery)
