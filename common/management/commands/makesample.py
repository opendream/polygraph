from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from datetime import timedelta
from account.models import Staff
from common import factory
from common.constants import STATUS_PENDING, STATUS_PUBLISHED, STATUS_DRAFT

import time

class Command(BaseCommand):

    help = 'Make example data'


    def handle(self, *args, **options):

        for i in range(1, 30):
            outdate = timezone.now() - timedelta(days=settings.UPTODATE_DAYS + 1 + i)
            factory.create_statement(status=STATUS_PUBLISHED, created=outdate, created_raw=outdate, use_log_description=True)


        outdate = timezone.now() - timedelta(days=settings.UPTODATE_DAYS + 1)

        factory.create_statement(status=STATUS_DRAFT, created=outdate, created_raw=outdate, created_by=Staff.objects.get(id=1))
        factory.create_statement(status=STATUS_PENDING, created=outdate, created_raw=outdate)
        factory.create_statement(status=STATUS_PUBLISHED, created=outdate, created_raw=outdate)

        statement1 = factory.create_statement(status=STATUS_PUBLISHED, use_log_description=True)
        statement3 = factory.create_statement(status=STATUS_PUBLISHED, use_log_description=True)

        statement1.save()

        time.sleep(1)
        factory.create_statement(created=timezone.now(), status=STATUS_PUBLISHED, use_log_description=True)

        statement3.save()
