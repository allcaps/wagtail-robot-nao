# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 00:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import home.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', models.TextField(blank=True)),
                ('body', wagtail.wagtailcore.fields.StreamField([(b'h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.RichTextBlock()), (b'alignment', home.models.ImageFormatChoiceBlock())], icon='image', label='Image'))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
