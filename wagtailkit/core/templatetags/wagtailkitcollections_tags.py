from django import template
from django.core.paginator import Page, Paginator
from wagtail.core.models import Collection, GroupCollectionPermission
from wagtail.documents.models import Document

register = template.Library()


# get a user's collections based_on their groups
@register.simple_tag(takes_context=True)
def get_user_collections(context):
    user = context['request'].user
    collections = Collection.objects.all()
    if not user.is_superuser:
        groups = user.groups.all()
        if groups:
            collection_permissions = GroupCollectionPermission.objects.filter(group__in=groups)
            if collection_permissions:
                collection_pks = [cp.collection.pk for cp in collection_permissions.all()]
                collections = collections.filter(pk__in=collection_pks)
    return collections