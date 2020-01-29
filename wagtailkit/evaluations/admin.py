from django.contrib import admin

from .models import (
    EvalQuestion, EvalQuestionGroup, Evaluation)


@admin.register(EvalQuestion)
class EvalQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(EvalQuestionGroup)
class EvalQuestionGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    pass