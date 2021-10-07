from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CuponConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cupon'
    verbose_name = _('cupon')