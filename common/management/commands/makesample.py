from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from datetime import timedelta
from common import factory


class Command(BaseCommand):

    help = 'Make example data'


    def handle(self, *args, **options):

        for i in range(1, 30):
            outdate = timezone.now() - timedelta(days=settings.UPTODATE_DAYS + 1 + i)
            factory.create_statement(created=outdate, use_log_description=True)

        statement1 = factory.create_statement(use_log_description=True)
        statement2 = factory.create_statement(use_log_description=True)
        statement3 = factory.create_statement(use_log_description=True)

        statement1.save()
        statement3.save()