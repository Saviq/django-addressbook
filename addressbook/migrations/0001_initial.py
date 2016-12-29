# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('is_company', models.BooleanField(default=False, verbose_name='company')),
                ('photo', models.ImageField(upload_to=b'var/addressbook/photos', verbose_name='photo', blank=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
            },
        ),
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('value', models.TextField(verbose_name='value')),
                ('contact', models.ForeignKey(related_name='custom_fields', to='addressbook.Contact')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('value', models.DateField(verbose_name='date')),
                ('contact', models.ForeignKey(related_name='dates', to='addressbook.Contact')),
            ],
            options={
                'verbose_name': 'date',
                'verbose_name_plural': 'dates',
            },
        ),
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_primary', models.BooleanField(default=False, verbose_name='primary')),
                ('label', models.CharField(max_length=200, verbose_name='label', choices=[(b'home', 'home'), (b'work', 'work'), (b'other', 'other')])),
                ('name', models.CharField(max_length=200, verbose_name='name', blank=True)),
                ('value', models.EmailField(max_length=254, verbose_name='address')),
                ('contact', models.ForeignKey(related_name='email_addresses', to='addressbook.Contact')),
            ],
            options={
                'verbose_name': 'email address',
                'verbose_name_plural': 'email addresses',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('members', models.ManyToManyField(to='addressbook.Contact', null=True, verbose_name='members', blank=True)),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
        ),
        migrations.CreateModel(
            name='IMAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_primary', models.BooleanField(default=False, verbose_name='primary')),
                ('service', models.CharField(max_length=30, verbose_name='service', choices=[(b'google', 'Google Talk'), (b'aim', 'AIM'), (b'yahoo', 'Yahoo'), (b'msn', 'MSN'), (b'icq', 'ICQ'), (b'jabber', 'Jabber')])),
                ('account', models.CharField(help_text='user name or email address', max_length=200, verbose_name='account')),
                ('contact', models.ForeignKey(related_name='im_accounts', to='addressbook.Contact')),
            ],
            options={
                'verbose_name': 'IM account',
                'verbose_name_plural': 'IM accounts',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('value', models.URLField(default=b'http://', verbose_name='URL')),
                ('contact', models.ForeignKey(related_name='links', to='addressbook.Contact')),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_primary', models.BooleanField(default=False, verbose_name='primary')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('title', models.CharField(max_length=200, verbose_name='title', blank=True)),
                ('contact', models.ForeignKey(related_name='organizations', to='addressbook.Contact')),
            ],
            options={
                'verbose_name': 'organization',
                'verbose_name_plural': 'organizations',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_primary', models.BooleanField(default=False, verbose_name='primary')),
                ('name', models.CharField(max_length=200, verbose_name='name', blank=True)),
                ('label', models.CharField(max_length=200, verbose_name='label', choices=[(b'landline', 'landline'), (b'mobile', 'mobile'), (b'fax', 'fax')])),
                ('value', models.CharField(max_length=100, verbose_name='number')),
                ('contact', models.ForeignKey(related_name='phone_numbers', to='addressbook.Contact')),
            ],
            options={
                'verbose_name': 'phone number',
                'verbose_name_plural': 'phone numbers',
            },
        ),
        migrations.CreateModel(
            name='PostalAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_primary', models.BooleanField(default=False, verbose_name='primary')),
                ('label', models.CharField(max_length=200, verbose_name='label', choices=[(b'home', 'home'), (b'work', 'work'), (b'other', 'other')])),
                ('address1', models.CharField(max_length=127, verbose_name='address line 1')),
                ('address2', models.CharField(max_length=127, verbose_name='address line 2', blank=True)),
                ('city', models.CharField(max_length=127, verbose_name='city', blank=True)),
                ('state', models.CharField(max_length=127, verbose_name='state/province/region', blank=True)),
                ('country', models.CharField(max_length=127, verbose_name='country')),
                ('postcode', models.CharField(max_length=31, verbose_name='postal code/zip code', blank=True)),
                ('contact', models.ForeignKey(related_name='postal_addresses', to='addressbook.Contact')),
            ],
            options={
                'verbose_name': 'postal address',
                'verbose_name_plural': 'postal addresses',
            },
        ),
    ]
