from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Cupon(models.Model):
    code = models.CharField(max_length=50, unique=True,verbose_name=_('code'))
    valid_from = models.DateTimeField(verbose_name=_('valid_from'))
    valid_to = models.DateTimeField(verbose_name=_('valid_to'))
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],verbose_name=_('discount'))
    active = models.BooleanField(verbose_name=_('active'))
    is_used = models.BooleanField(verbose_name=_('is_used'),default=False)

    class Meta:
        ordering = ['id']
        verbose_name = _('Cupon')
        verbose_name_plural = _('Cupons')

    @property
    def active(self):
        if timezone.now() > self.valid_to:
            return False
        return True

    def __str__(self):
        return self.code
