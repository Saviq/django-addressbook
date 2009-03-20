import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from imagekit.models import ImageModel


PROPERTY_LABELS = (
    ('home', 'home'),
    ('work', 'work'),
    ('other', 'other'),
)

IM_SERVICES = (
    ('google', 'Google Talk'),
    ('aim', 'AIM'),
    ('yahoo', 'Yahoo'),
    ('msn', 'MSN'),
    ('icq', 'ICQ'),
    ('jabber', 'Jabber'),
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
        self.contact.date_modified = datetime.datetime.now()
        self.contact.save()
        models.Model.save(self, *args, **kwargs)


class PrimaryProperty(ContactProperty):
    is_primary = models.BooleanField(default=False)
    
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
    label = models.CharField(max_length=200, choices=PROPERTY_LABELS)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return u'%s [%s]' % (self.value, LabeledProperty.get_label_display(self))

    
class NamedProperty(models.Model):
    name = models.CharField(max_length=200)
    
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
    value = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.label, self.value)


class Date(ContactProperty, NamedProperty):
    contact = models.ForeignKey('Contact', related_name="dates")
    value = models.DateField('date')


class EmailAddress(PrimaryProperty, LabeledProperty):
    contact = models.ForeignKey('Contact', related_name="email_addresses")
    value = models.EmailField('address')

    class Meta:
        verbose_name_plural = 'email addresses'


class IMAccount(ContactProperty):
    contact = models.ForeignKey('Contact', related_name="im_accounts")
    service = models.CharField(max_length=30, choices=IM_SERVICES)
    account = models.CharField('user name or email address', max_length=200)
    
    @property
    def value(self):
        return self.account
    
    class Meta:
        verbose_name = 'IM account'
        verbose_name_plural = 'IM accounts'


class Link(ContactProperty, NamedProperty):
    contact = models.ForeignKey('Contact', related_name="links")
    value = models.URLField('URL', max_length=200, default='http://')
        
    def save(self, *args, **kwargs):
        if self.value == 'http://':
            return
        super(Link, self).save(*args, **kwargs)


class Organization(PrimaryProperty):
    contact = models.ForeignKey('Contact', related_name="organizations")
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return ', '.join([s for s in [self.name, self.title] if len(s)])


class PhoneNumber(PrimaryProperty):
    PHONE_NUM_LABELS = (
        ('home', 'home'),
        ('work', 'work'),
        ('home fax', 'home fax'),
        ('work fax', 'work fax'),
        ('mobile', 'mobile'),
        ('other', 'other'),
    )
    contact = models.ForeignKey('Contact', related_name="phone_numbers")
    label = models.CharField(max_length=200, choices=PHONE_NUM_LABELS)
    value = models.CharField('number', max_length=100)
    
    def __unicode__(self):
        return u'%s [%s]' % (self.value, PhoneNumber.get_label_display(self))
                                       

class PostalAddress(PrimaryProperty, LabeledProperty):
    contact = models.ForeignKey('Contact', related_name="postal_addresses")
    value = models.TextField('address')

    class Meta:
        verbose_name_plural = 'postal addresses'


class Contact(ImageModel):
    """ An person, company, etc.
    
    """
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='addressbook/photos', blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(default=datetime.datetime.now,
                                        editable=False)
    date_updated = models.DateTimeField(default=datetime.datetime.now,
                                        editable=False)

    class Meta:
        ordering = ('name',)
        
    class IKOptions:
        image_field = 'photo'
        spec_module = 'addressbook.specs'
        cache_dir = 'cache/addressbook'

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
        return ', '.join([s.strip() for s in \
                          str(self.postal_address).split('\n')])

    def save(self, *args, **kwargs):
        self.date_updated = datetime.datetime.now()
        super(Contact, self).save(*args, **kwargs)


class Group(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(Contact, null=True, blank=True)
        
    @property
    def member_list(self):
        return ', '.join([str(c) for c in self.members.all()[:5]])

    def __unicode__(self):
        return self.name
