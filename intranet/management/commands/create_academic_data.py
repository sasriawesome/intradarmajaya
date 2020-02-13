from django.core.management import CommandError, BaseCommand
from ._academic_initial_data import (
    clean_course_type, clean_rmu_roots, clean_course_group,
    create_course_type, create_rmu_roots, create_course_group,
    clean_school_year, create_school_year
)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='clean',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        try:
            if options['clean']:
                clean_rmu_roots()
                clean_course_type()
                clean_course_group()
                clean_school_year(),
            create_school_year()
            create_rmu_roots()
            create_course_type()
            create_course_group()
        except Exception as err:
            raise CommandError(err)

        self.stdout.write(self.style.SUCCESS('Successfully install academic initial data.'))