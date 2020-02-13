from django.core.management import CommandError, BaseCommand
from ._academic_initial_data import (
    clean_course_type, clean_rmu_roots, clean_course_group,
    clean_school_year
)

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            clean_course_type()
            clean_rmu_roots()
            clean_course_group()
            clean_school_year()
        except Exception as err:
            raise CommandError(err)

        self.stdout.write(self.style.SUCCESS('Successfully clean academic initial data.'))