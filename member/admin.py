from django.contrib import admin

from member.models import TeamManagers, UserMember, Payments, Player, User

admin.site.unregister(User)


def make_player_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


def make_player_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


def change_password(modeladmin, request, queryset):
    queryset.update(password="pbkdf2_sha256$30000$tmJztDx7lgtg$CrOItg+7R2H2y+9VjZX9yY5xbP9zw8oGAxxC7Pn704w=")


make_player_active.short_description = "Make Selected Players Active - WGS"
make_player_inactive.short_description = "Make Selected Players Inactive - WGS"
change_password.short_description = "Set Temporary Password"


@admin.register(UserMember)
class UserMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'address1', 'address2', 'postcode',)
    search_fields = ('full_name', )

pass


@admin.register(TeamManagers)
class TeamManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team', 'email', 'mobile_phone', 'game_format', )
    list_filter = ('game_format', )

pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined')
    list_filter = ('date_joined',)
    search_fields = ('first_name', 'email', 'username')
    actions = [change_password, ]

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
    search_fields = ('name', )
    actions = [make_player_active, make_player_inactive]

pass
