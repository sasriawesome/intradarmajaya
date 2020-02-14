from django.contrib import admin

from .models import Numerator


@admin.register(Numerator)
class NumeratorAdmin(admin.ModelAdmin):
    list_display = ['ctype', 'dtype', 'date_start', 'date_end', 'counter']