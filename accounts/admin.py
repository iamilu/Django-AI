from django.contrib import admin
from .models import Account, UserProfile

from django.contrib.auth.admin import UserAdmin

# Register your models here.
'''
write an Account Admin model to with the list of display fields name
email, username, first_name, last_name, date_joined, last_login, is_active
'''
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile)