from django.db import models
from django.contrib.auth.models import Group, Permission
from wagtail.core import hooks
from wagtail.core.models import (
    Collection,
    GroupCollectionPermission,
    CollectionViewRestriction
)


@hooks.register('after_create_user')
def create_group_and_collection_for_user(request, user):
    """ Create private collection and group for given User """

    group_prefix = 'USER_GROUP_'
    collection_prefix = 'USER_COLLECTION_'

    # create user's private_group and bind to user
    group_name = '%s_%s_%s' % (group_prefix, user.username, str(user.id).replace('-','')[0:8])
    group, new_group = Group.objects.get_or_create(
        name=group_name,
        defaults={'name': group_name}
    )

    # create user's private_collection
    collection_name = '%s_%s_%s' % (collection_prefix, user.username, str(user.id).replace('-','')[0:8])
    collection = Collection(name=collection_name)
    root_collection = Collection.get_first_root_node()
    root_collection.add_child(instance=collection)

    # add group collection permissions
    permissions = Permission.objects.filter(
        codename__in=['add_image', 'add_document']
    )
    group_object_permissions = []
    for perm in permissions:
        group_object_permissions.append(
            GroupCollectionPermission(
                group=group,
                collection=collection,
                permission=perm
            )
        )
    GroupCollectionPermission.objects.bulk_create(
        group_object_permissions
    )

    # Setup CollectionViewRestriction to private for user's group
    restriction = CollectionViewRestriction.objects.create(
        restriction_type=CollectionViewRestriction.GROUPS,
        collection=collection
    )
    restriction.groups.add(group)
    restriction.save()

    group.user_set.add(user)


def get_user_collections(request):
    """ Get user collections queryset """
    user = request.user
    collections = Collection.objects.all()
    if not user.is_superuser:
        groups = user.groups.all()
        if groups:
            collection_permissions = GroupCollectionPermission.objects.filter(group__in=groups)
            if collection_permissions:
                collection_pks = [cp.collection.pk for cp in collection_permissions.all()]
                collections = collections.filter(pk__in=collection_pks)
    return collections


@hooks.register('construct_document_chooser_queryset')
def document_chooser_based_on_collection_permissions(documents, request):
    """ Only show documents and collections owned by user """
    if request.user.is_superuser:
        return documents

    documents = documents.filter(
        models.Q(collection__in=get_user_collections(request))
        & models.Q(uploaded_by_user=request.user)
    )
    return documents


@hooks.register('construct_image_chooser_queryset')
def image_chooser_based_on_collection_permissions(images, request):
    """ Only show images and collections owned by user """
    if request.user.is_superuser:
        return images

    images = images.filter(
        models.Q(collection__in=get_user_collections(request))
        & models.Q(uploaded_by_user=request.user)
    )
    return images
