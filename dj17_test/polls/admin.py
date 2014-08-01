from __future__ import absolute_import
from django.contrib import admin

from .models import Question, Choice, Vote

admin.site.register(Vote, admin.ModelAdmin)
admin.site.register(Question, admin.ModelAdmin)
admin.site.register(Choice, admin.ModelAdmin)
