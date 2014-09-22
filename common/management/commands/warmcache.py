from django.core.management import BaseCommand
from common.tasks import warm_cache

class Command(BaseCommand):

    help = 'Warn redis cache for anonymous users'

    def handle(self, *args, **options):

        warm_cache.delay()