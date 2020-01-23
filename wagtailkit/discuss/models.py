import uuid

from django.db import models
from django.utils import translation, timezone
from django.shortcuts import reverse
from django.conf import settings

from wagtail.core.models import Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.documents.models import Document
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase
from mptt.models import MPTTModel, TreeForeignKey

_ = translation.gettext_lazy


class DiscussionTag(TaggedItemBase):
    content_object = ParentalKey(
        'Discussion',
        related_name='tagged_discussions',
        on_delete=models.CASCADE
    )


@register_snippet
class DiscussionCategory(MPTTModel):
    class Meta:
        verbose_name = _('Discussion Category')
        verbose_name_plural = _('Discussion Categories')

    parent = TreeForeignKey(
        'discuss.DiscussionCategory',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Parent'))
    name = models.CharField(max_length=125, verbose_name=_('Name'))
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name=_('Description'))

    def __str__(self):
        return self.name

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('description')
        ])
    ]


class Discussion(ClusterableModel, models.Model):
    class Meta:
        verbose_name = _('Discussion')
        verbose_name_plural = _('Discussions')
        ordering = ['-date_created']
        permissions = (
            ('changeother_discussion', _('Can change other Discussion')),
            ('deleteother_discussion', _('Can delete other Discussion')),
        )
    PUBLISHED = 'published'
    UNPUBLISHED = 'unpublished'
    TRASH = 'trash'
    STATUS = (
        (PUBLISHED, _('Published')),
        (UNPUBLISHED, 'Unpublished'),
        (TRASH, 'Trash')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    date_created = models.DateTimeField(default=timezone.now, verbose_name=_('Title'))
    date_modified = models.DateTimeField(default=timezone.now, verbose_name=_('Title'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    summary = RichTextField(null=True, blank=True, max_length=500, verbose_name=_('Summary'))
    body = RichTextField(max_length=10000, verbose_name=_('Body'))
    category = TreeForeignKey(
        DiscussionCategory,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Category'))
    tags = ClusterTaggableManager(through=DiscussionTag, blank=True)
    attachment = models.ForeignKey(
        Document, related_name='file_attachment', null=True, blank=True,
        on_delete=models.SET_NULL, verbose_name=_('File attachment'))
    status = models.CharField(choices=STATUS, default=UNPUBLISHED, max_length=20, verbose_name=_('Status'))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Creator'))
    show_comment = models.BooleanField(default=True, verbose_name=_('Show comment'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('%s_%s_modeladmin_inspect' % (self._meta.app_label, self._meta.model_name), args=(self.id,))


class DiscussionGalleryImage(Orderable):
    page = ParentalKey(Discussion, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

    def __str__(self):
        return self.caption
