# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

STATUS_PUBLISHED = 1
STATUS_PENDING = -1
STATUS_DRAFT = 0

STATUS_CHOICES = (
    (STATUS_PUBLISHED, _('Published')),
    (STATUS_PENDING, _('Pending Review')),
    (STATUS_DRAFT, _('Draft')),
)

THAI_MONTH_NAME = ('', 'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม')
THAI_MONTH_ABBR_NAME = ('', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.')

NO_IP = '127.0.0.1'