from django.contrib import admin
from .models import Account, UserProfile

from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

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

'''
write a UserProfile Admin model to with the list of display fields name
and function to create thumbnal, full_name, email, phone
'''
class UserProfileAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html('<img src="{}" height="40" width="40" style="border-radius:50%;">'.format(object.profile_pic.url))
    thumbnail.short_description = 'Profile Picture'

    def full_name(self, object):
        return object.user.first_name.capitalize() + ' ' + object.user.last_name.capitalize()
    full_name.short_description = 'Name'

    def email(self, object):
        return object.user.email
    email.short_description = 'Email Address'

    def phone(self, object):
        return object.user.phone
    phone.short_description = 'Phone Number'

    list_display = ['thumbnail', 'full_name', 'user', 'phone', 'city', 'pincode', 'state', 'country']

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)