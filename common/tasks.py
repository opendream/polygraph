from django.conf import settings
from celery import task


@task()
def warm_cache():

    if settings.MAINTENANCE_MODE:
        return False

    from django.test.client import Client
    from django.core.urlresolvers import reverse
    from domain.models import Meter, Statement, People, PeopleCategory
    from domain.views import statement_query_base, people_query_base
    from common.constants import STATUS_DRAFT, STATUS_PENDING


    client = Client()
    client.get(reverse('home'))
    client.get(reverse('statement_list'))
    client.get(reverse('people_list'))
    client.get(reverse('meter_detail_default'))

    for meter in Meter.objects.all():
        client.get(reverse('meter_detail', args=[meter.permalink]))

    # TODO: Flag extra warm when only cron run
    if True:

        for category in PeopleCategory.objects.all():
            client.get(reverse('people_list'), {'category': category.permalink})

        for statement in Statement.objects.exclude(status__in=[STATUS_DRAFT, STATUS_PENDING]).order_by('-hilight', '-promote', '-changed', '-created')[0:20]:
            client.get(reverse('statement_detail', args=[statement.permalink]))

        for people in People.objects.exclude(status__in=[STATUS_DRAFT, STATUS_PENDING]).order_by('-quoted_by__created')[0:20]:
            client.get(reverse('people_detail', args=[people.permalink]))
