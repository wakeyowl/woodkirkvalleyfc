from django.contrib import admin

from member.models import TeamManagers, UserMember, Payments, Player, User

admin.site.unregister(User)


def make_player_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


def make_player_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)

make_player_active.short_description = "Make Selected Players Active - WGS"
make_player_inactive.short_description = "Make Selected Players Inactive - WGS"


@admin.register(UserMember)
class UserMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'address1', 'address2', 'postcode',)


pass


@admin.register(TeamManagers)
class TeamManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team', 'email', 'mobile_phone',)


pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined')
    list_filter = ('date_joined',)

pass


@admin.register(Payments)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'payment_amount', 'date_taken', 'paymentType', 'manager')
    list_filter = ('paymentType', 'manager',)


pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birthdate', 'medical_details', 'member_parent_id', 'is_active', 'manager_id',
                    'picture',)
    list_filter = ('manager_id', 'is_active')
    actions = [make_player_active, make_player_inactive]


pass
