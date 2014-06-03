from django.utils.translation import ugettext_lazy as _

STATUS_PUBLISHED = 1
STATUS_PENDING = -1
STATUS_DRAFT = 0

STATUS_CHOICES = (
    (STATUS_PUBLISHED, _('Published')),
    #(STATUS_PENDING, _('Pending')),
    (STATUS_DRAFT, _('Draft')),
)