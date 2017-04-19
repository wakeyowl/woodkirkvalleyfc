from django.contrib import admin
from member.models import BadgeAwards, Badges


class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ('userId_id', 'badgeId_id', 'dateAwarded')


class BadgesAdmin(admin.ModelAdmin):
    list_display2 = ('name', 'category', 'levels')

    class Meta:
        verbose_name_plural = "badges"

admin.site.register(BadgeAwards, BadgeAwardAdmin)
admin.site.register(Badges, BadgesAdmin)
