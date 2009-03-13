from django.contrib import admin
from django.contrib.contenttypes import generic

from models import *

class InlineCustomField(generic.GenericTabularInline):
    model = CustomField
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class InlineDate(generic.GenericTabularInline):
    model = Date
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class InlineEmailAddress(generic.GenericTabularInline):
    model = EmailAddress
    extra = 2
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class InlineIMAccount(generic.GenericTabularInline):
    model = IMAccount
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class InlineLink(generic.GenericTabularInline):
    model = Link
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class InlineOrganization(generic.GenericTabularInline):
    model = Organization
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class InlinePhoneNumber(generic.GenericTabularInline):
    model = PhoneNumber
    extra = 2
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class InlinePostalAddress(generic.GenericTabularInline):
    model = PostalAddress
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'company',
                    'email_address',
                    'im_account',
                    'phone_number',
                    'address',
                    'admin_thumbnail_view')
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


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'member_list')
    search_fields = ['name', 'description']
    filter_horizontal = ('members',)


admin.site.register(Contact, ContactAdmin)
admin.site.register(Group, GroupAdmin)
