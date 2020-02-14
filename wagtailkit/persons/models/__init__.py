from .extra import Address, ContactInfo, KKNILevel
from .person import Person, PersonAddress, PersonManager
from .histories import (
    FormalEducation, NonFormalEducation, Working,
    Volunteer, Skill, Publication, Family, Award)
from .settings import PersonSettings

from wagtail.contrib.settings.registry import register_setting

register_setting(PersonSettings, icon='group')
