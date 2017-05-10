from django.contrib import admin

from member.models import TeamManagers, UserMember, Payments, Player


class UserMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name',)


class TeamManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'payment_amount', 'date_taken', 'paymentType', )
    list_filter = ('player_id', 'paymentType',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birthdate', 'medical_details', 'member_parent_id', 'is_active', 'manager_id')
    list_filter = ('manager_id', 'is_active',)

admin.site.register(Payments, PaymentAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(UserMember, UserMemberAdmin)
admin.site.register(TeamManagers, TeamManagerAdmin)

