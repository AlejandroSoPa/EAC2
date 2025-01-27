from django.contrib import admin
from .models import *

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    inlines = [ChoiceInline]
    search_fields = ["question_text"]
    list_filter = ["pub_date"]

admin.site.register(Question, QuestionInLine)
admin.site.register(Choice)
