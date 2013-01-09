from django.contrib import admin
from django.contrib.contenttypes import generic

from imagekit.admin import AdminThumbnail

from models import *


class InlineCustomField(admin.TabularInline):
    model = CustomField
    extra = 1

class InlineDate(admin.TabularInline):
    model = Date
    extra = 1

class InlineEmailAddress(admin.TabularInline):
    model = EmailAddress
    extra = 2

class InlineIMAccount(admin.TabularInline):
    model = IMAccount
    extra = 1

class InlineLink(admin.TabularInline):
    model = Link
    extra = 1

class InlineOrganization(admin.TabularInline):
    model = Organization
    extra = 1

class InlinePhoneNumber(admin.TabularInline):
    model = PhoneNumber
    extra = 2

class InlinePostalAddress(admin.StackedInline):
    model = PostalAddress
    extra = 1


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'company',
                    'email_address',
                    'im_account',
                    'phone_number',
                    'address',
                    'admin_thumbnail')
    search_fields = ['name',
                     'notes']
    inlines = [
        InlinePhoneNumber,
        InlineEmailAddress,
        InlinePostalAddress,
        InlineOrganization,
        InlineLink,
        InlineIMAccount,
        InlineDate,
        InlineCustomField,
    ]
    admin_thumbnail = AdminThumbnail(image_field='photo')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'member_list')
    search_fields = ['name', 'description']
    filter_horizontal = ('members',)


admin.site.register(Contact, ContactAdmin)
admin.site.register(Group, GroupAdmin)
