from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .types import (
    PersonNode
)

from wagtailkit.persons.models import Person


class PersonQuery(ObjectType):
    person = relay.Node.Field(PersonNode)
    all_persons = DjangoFilterConnectionField(PersonNode)
