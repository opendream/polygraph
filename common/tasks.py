
from celery import task


@task()
def warm_cache():

    from django.test.client import Client
    from django.core.urlresolvers import reverse
    from domain.models import Meter

    client = Client()
    client.get(reverse('home'))
    client.get(reverse('statement_list'))
    client.get(reverse('people_list'))
    client.get(reverse('meter_detail_default'))

    for meter in Meter.objects.all():
        client.get(reverse('meter_detail', args=[meter.permalink]))