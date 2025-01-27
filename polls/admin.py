from django.contrib import admin
from .models import *

# Register your models here.

class QuestionInLine(admin.ModelAdmin):
    list_display = ["choice_text"]

admin.site.register(Question, QuestionInLine)
admin.site.register(Choice)
