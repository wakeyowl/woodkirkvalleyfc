from django.contrib import admin

from member.models import TeamManagers, UserMember, Payments, Player


class UserMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name',)


class TeamManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team')


admin.site.register(Payments)
admin.site.register(Player)
admin.site.register(UserMember, UserMemberAdmin)
admin.site.register(TeamManagers, TeamManagerAdmin)

