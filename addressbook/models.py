from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from imagekit.models import ImageModel


PROPERTY_LABELS = (
    ('home', _('home')),
    ('work', _('work')),
    ('other', _('other')),
)

IM_SERVICES = (
    ('google', _('Google Talk')),
    ('aim', _('AIM')),
    ('yahoo', _('Yahoo')),
    ('msn', _('MSN')),
    ('icq', _('ICQ')),
    ('jabber', _('Jabber')),
)


class PrimaryPropertyManager(models.Manager):
    def primary(self):
        try:
            return self.get_query_set().get(is_primary=True)
        except ObjectDoesNotExist:
            return None
           
# Base classes
# Every contact property must inherit from either ContactProperty or
# PrimaryPropery 
            
class ContactProperty(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.contact.save()
        models.Model.save(self, *args, **kwargs)


class PrimaryProperty(ContactProperty):
    is_primary = models.BooleanField(_("primary"), default=False)
    
    objects = PrimaryPropertyManager()
        
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        update_primary = kwargs.pop('update_primary', True)
        if update_primary:
            try:
                existing = self.__class__.objects.exclude(pk=self.id) \
                                                 .filter(contact=self.contact,
                                                         is_primary=True).get()
            except ObjectDoesNotExist:
                existing = None
            if self.is_primary:
                if existing is not None:
                    existing.is_primary = False
                    existing.save(update_primary=False)
            elif existing is None:
                self.is_primary = True
        super(PrimaryProperty, self).save(*args, **kwargs)


# Mixin classes
# Abstacts out common fields and methods, models can implement this for
# themselves if different.

class LabeledProperty(models.Model):
    label = models.CharField(_("label"), max_length=200, choices=PROPERTY_LABELS)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return u'%s [%s]' % (self.value, LabeledProperty.get_label_display(self))

    
class NamedProperty(models.Model):
    name = models.CharField(_("name"), max_length=200)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return u'%s: %s' % (self.name, self.value)

        
# Contact properties

class PrimaryPropertyDescriptor(object):
    def __init__(self, collection_name):
        self.collection_name = collection_name
        
    def get_collection(self, instance):
        return getattr(instance, self.collection_name)
        
    def __get__(self, instance, owner):
        if instance is None:
            return None
        return self.get_collection(instance).primary()
        
    def __set__(self, instance, value):
        value.is_primary = True
        self.get_collection(instance).add(value)
        
    def __delete__(self, instance):
        self.get_collection(instance).primary().delete()
        for obj in self.get_collection(instance).all():
            obj.is_primary = True
            return
            
            
class CustomField(ContactProperty, NamedProperty):
    contact = models.ForeignKey('Contact', related_name="custom_fields")
    value = models.TextField(_("value"))

    def __unicode__(self):
        return u'%s: %s' % (self.name, self.value)


class Date(ContactProperty, NamedProperty):
    contact = models.ForeignKey('Contact', related_name="dates")
    value = models.DateField(_("date"))
    
    class Meta:
        verbose_name = _("date")
        verbose_name_plural = _("dates")

class EmailAddress(PrimaryProperty, LabeledProperty):
    contact = models.ForeignKey('Contact', related_name="email_addresses")
    value = models.EmailField(_("address"))

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")


class IMAccount(ContactProperty):
    contact = models.ForeignKey('Contact', related_name="im_accounts")
    service = models.CharField(_("service"), max_length=30, choices=IM_SERVICES)
    account = models.CharField(_("account"), help_text=_("user name or email address"), max_length=200)
    
    class Meta:
        verbose_name = _("IM account")
        verbose_name_plural = _("IM accounts")
            
    @property
    def value(self):
        return self.account


class Link(ContactProperty, NamedProperty):
    contact = models.ForeignKey('Contact', related_name="links")
    value = models.URLField(_('URL'), max_length=200, default='http://')

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
                
    def save(self, *args, **kwargs):
        if self.value == 'http://':
            return
        super(Link, self).save(*args, **kwargs)


class Organization(PrimaryProperty):
    contact = models.ForeignKey('Contact', related_name="organizations")
    name = models.CharField(_("name"), max_length=200)
    title = models.CharField(_("title"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
            
    def __unicode__(self):
        return self.name


class PhoneNumber(PrimaryProperty):
    PHONE_NUM_LABELS = (
        ('home', _('home')),
        ('work', _('work')),
        ('home fax', _('home fax')),
        ('work fax', _('work fax')),
        ('mobile', _('mobile')),
        ('other', _('other')),
    )
    contact = models.ForeignKey('Contact', related_name="phone_numbers")
    label = models.CharField(_("label"), max_length=200, choices=PHONE_NUM_LABELS)
    value = models.CharField(_('number'), max_length=100)

    class Meta:
        verbose_name = _("phone number")
        verbose_name_plural = _("phone numbers")
            
    def __unicode__(self):
        return u'%s [%s]' % (self.value, PhoneNumber.get_label_display(self))
                                       

class PostalAddress(PrimaryProperty, LabeledProperty):
    contact = models.ForeignKey('Contact', related_name="postal_addresses")
    address1 = models.CharField(_("address line 1"), max_length=127, blank=False)
    address2 = models.CharField(_("address line 2"), max_length=127, blank=True)
    city = models.CharField(_("city"), max_length=127, blank=True)
    state = models.CharField(_("state/province/region"), max_length=127, blank=True)
    country = models.CharField(_("country"), max_length=127)
    postcode = models.CharField(_("postal code/zip code"), max_length=31, blank=True)

    class Meta:
        verbose_name = _("postal address")
        verbose_name_plural = _("postal addresses")
        
    @property
    def value(self):
        data = [self.address1, self.address2, self.city,
                self.state, self.country, self.postcode]
        return ", ".join([i for i in data if i])


class Contact(ImageModel):
    """ A person or company.
    
    """
    name = models.CharField(max_length=200)
    is_company = models.BooleanField(_("company"), default=False)
    photo = models.ImageField(_("photo"), upload_to='var/addressbook/photos', blank=True)
    notes = models.TextField(_("notes"), blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")
        ordering = ('name',)
        
    class IKOptions:
        image_field = 'photo'
        spec_module = 'addressbook.specs'
        cache_dir = 'var/cache/addressbook'

    def __unicode__(self):
        return self.name
        
    # primary contact properies
    email_address = PrimaryPropertyDescriptor('email_addresses')
    im_account = PrimaryPropertyDescriptor('im_accounts')
    company = PrimaryPropertyDescriptor('organizations')
    phone_number = PrimaryPropertyDescriptor('phone_numbers')
    postal_address = PrimaryPropertyDescriptor('postal_addresses')
    
    @property
    def address(self):
        return self.postal_address


class Group(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(_("description"), blank=True)
    members = models.ManyToManyField(Contact, verbose_name=_("members"), null=True, blank=True)
        
    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        
    @property
    def member_list(self):
        return ', '.join([str(c) for c in self.members.all()[:5]])

    def __unicode__(self):
        return self.name
