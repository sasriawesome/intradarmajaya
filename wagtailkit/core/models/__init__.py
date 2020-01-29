from wagtail.contrib.settings.models import register_setting

from .base import KitBaseModel, CreatorModelMixin, MetaFieldMixin, SignalAwareClusterableModel
from .settings import CompanySettings
from .mixins import (
    StatusMixin, ThreeStepStatusMixin, FourStepStatusMixin,
    FiveStepStatusMixin, CloseStatusMixin
)

MAX_LEN_SHORT = 128
MAX_LEN_MEDIUM = 256
MAX_LEN_LONG = 512
MAX_LEN_XLONG = 1024
MAX_LEN_TEXT = 2048
MAX_RICHTEXT = 10000

register_setting(CompanySettings, icon='cogs')
