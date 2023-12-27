from django.contrib import admin
from ASKII.models import Question
from ASKII.models import Tag
from ASKII.models import Profile
from ASKII.models import Answer
from ASKII.models import QuestionLike
from ASKII.models import AnswerLike

# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    pass

