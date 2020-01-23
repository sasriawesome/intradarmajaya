from graphene import relay
from graphene_django import DjangoObjectType

from wagtailkit.persons.models import (
    Person, Skill, Award,
    FormalEducation, NonFormalEducation,
    Volunteer, Working, Family, PersonAddress,
    ContactInfo, Publication, EducationLevel
)


class PersonNode(DjangoObjectType):
    class Meta:
        model = Person
        filter_fields = {
            'fullname': ['icontains']
        }
        interfaces = (relay.Node,)


class SkillType(DjangoObjectType):
    class Meta:
        model = Skill


class AwardType(DjangoObjectType):
    class Meta:
        model = Award


class FormalEducationType(DjangoObjectType):
    class Meta:
        model = FormalEducation


class NonFormalEducationType(DjangoObjectType):
    class Meta:
        model = NonFormalEducation


class VolunteerType(DjangoObjectType):
    class Meta:
        model = Volunteer


class WorkingType(DjangoObjectType):
    class Meta:
        model = Working


class FamilyType(DjangoObjectType):
    class Meta:
        model = Family


class PersonAddressType(DjangoObjectType):
    class Meta:
        model = PersonAddress


class ContactInfoType(DjangoObjectType):
    class Meta:
        model = ContactInfo


class PublicationType(DjangoObjectType):
    class Meta:
        model = Publication


class EducationLevelType(DjangoObjectType):
    class Meta:
        model = EducationLevel
