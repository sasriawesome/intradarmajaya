from django.contrib import admin

from .models import (
    EvalQuestion, EvalQuestionGroup, Evaluation,
    LectureEvaluation, LectureEvaluationScore
)


@admin.register(EvalQuestion)
class EvalQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(EvalQuestionGroup)
class EvalQuestionGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    pass



class LectureEvaluationScoreLine(admin.TabularInline):
    extra = 0
    model = LectureEvaluationScore
    radio_fields = {"score": admin.HORIZONTAL, }
    readonly_fields = ['question']


@admin.register(LectureEvaluation)
class LectureEvaluationAdmin(admin.ModelAdmin):
    save_as = True
    search_fields = ['student__person__fullname', 'lecture__name']
    inlines = [LectureEvaluationScoreLine]
