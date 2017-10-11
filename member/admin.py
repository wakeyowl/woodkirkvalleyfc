from django.contrib import admin
from django.http import HttpResponse

from member.models import TeamManagers, UserMember, Payments, Player, User

admin.site.unregister(User)


# Export CSV fucntion added to Django
def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"Payment Amount"),
        smart_str(u"Description"),
        smart_str(u"Date Taken"),
        smart_str(u"Player"),
        smart_str(u"Manager"),
        smart_str(u"Payment Type"),

    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.payment_amount),
            smart_str(obj.description),
            smart_str(obj.date_taken),
            smart_str(obj.player),
            smart_str(obj.manager),
            smart_str(obj.paymentType),
        ])
    return response
export_csv.short_description = u"Export CSV"


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
    actions = [export_csv]

pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birthdate', 'medical_details', 'member_parent_id', 'is_active', 'manager_id',
                    'picture',)
    list_filter = ('manager_id', 'is_active')
    search_fields = ('name', )
    actions = [make_player_active, make_player_inactive]

pass
