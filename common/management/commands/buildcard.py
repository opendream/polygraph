from django.core.management import BaseCommand
from common.tasks import warm_cache

class Command(BaseCommand):

    help = 'Re generate statement cards (share image)'

    def handle(self, *args, **options):

        for s in Statement.objects.all():
            generate_statement_card('https://www.jabted.com/statement/%s/item/' % s.id, 'statement-card-%s.png' % s.id)
