from django.contrib import admin
from soccer.models import Team, Match

#
# class TeamAdmin(admin.ModelAdmin):
#     """ Show helpful fields on the changelist page. """
#     list_display = ('title', 'slug', 'author', 'created', 'modified')


admin.site.register(Team)
admin.site.register(Match)
