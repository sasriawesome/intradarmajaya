from django.contrib import admin
from wagtailkit.ememo.models import Memo

from .forms import MemoForm


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    form = MemoForm
    raw_id_fields = ['attachment']
