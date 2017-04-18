from django.contrib import admin
from member.models import BadgeUser, Badges


class BadgeUserAdmin(admin.ModelAdmin):
    list_display = ('dateAwarded', 'badgeId_id', 'userId_id')


class BadgesAdmin(admin.ModelAdmin):
    list_display2 = ('name', 'category', 'levels')

    class Meta:
        verbose_name_plural = "badges"

admin.site.register(BadgeUser, BadgeUserAdmin)
admin.site.register(Badges, BadgesAdmin)
