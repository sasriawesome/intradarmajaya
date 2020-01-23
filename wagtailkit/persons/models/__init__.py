from .extra import EducationLevel, Address, ContactInfo
from .person import Person, PersonAddress
from .histories import (
    FormalEducation, NonFormalEducation, Working, Volunteer, Skill, Publication, Family, Award
)
from .settings import PersonSettings

from wagtail.contrib.settings.registry import register_setting

register_setting(PersonSettings, icon='group')
