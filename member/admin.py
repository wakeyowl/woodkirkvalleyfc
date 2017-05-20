from django.contrib import admin

from member.models import TeamManagers, UserMember, Payments, Player


def make_player_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


make_player_active.short_description = "Make Selected Players Active"


@admin.register(UserMember)
class UserMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user',)


pass


@admin.register(TeamManagers)
class TeamManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team')


pass


@admin.register(Payments)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'payment_amount', 'date_taken', 'paymentType', 'manager')
    list_filter = ('paymentType', 'manager',)


pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birthdate', 'medical_details', 'member_parent_id', 'is_active', 'manager_id')
    list_filter = ('manager_id',)
    actions = [make_player_active]
pass
