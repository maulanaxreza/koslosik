from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.charge)
admin.site.register(models.pelanggan)
admin.site.register(models.penyewaan)
admin.site.register(models.detailcharge)
admin.site.register(models.kamar)