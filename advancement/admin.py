from django.contrib import admin
from advancement.models import Scouter, Parent, Rank, ScoutRank, MeritBadge, ScoutMeritBadge, MeritBadgeBook, ScoutMeritBadgeBook, MeritBadgeCounselor, ScoutNote, Requirement, ScoutRequirement

class ScouterAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'patrol')

admin.site.register(Scouter, ScouterAdmin)
admin.site.register(Parent)
admin.site.register(Rank)
admin.site.register(ScoutRank)
admin.site.register(MeritBadge)
admin.site.register(ScoutMeritBadge)
admin.site.register(MeritBadgeBook)
admin.site.register(ScoutMeritBadgeBook)
admin.site.register(MeritBadgeCounselor)
admin.site.register(ScoutNote)
admin.site.register(Requirement)
admin.site.register(ScoutRequirement)
