from celery import task
from django.conf import settings


@task()
def warm_cache():

    if settings.MAINTENANCE_MODE or settings.DEBUG:
        return False

    from django.test.client import Client
    from django.core.urlresolvers import reverse
    from domain.models import Meter, Statement, People, PeopleCategory
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

@task()
def generate_statement_card(url, filename):
    from pyvirtualdisplay import Display
    from selenium import webdriver
    from easyprocess import EasyProcessCheckInstalledError

    import os

    try:
        display = Display(visible=0, size=(settings.CARD_WIDTH, 200))
        display.start()
    except EasyProcessCheckInstalledError:
        pass

    browser = webdriver.Firefox()
    browser.window_handles
    browser.set_window_size(settings.CARD_WIDTH, 200)
    browser.get(url)

    card_dir = '%s/card/statement' % settings.MEDIA_ROOT
    if not os.path.isdir(card_dir):
        os.makedirs(card_dir)

    path = '%s/%s' % (card_dir, filename)
    if os.path.exists(path):
        os.remove(path)
 
    browser.save_screenshot(path)
    browser.quit()

    if display:
        display.stop()

