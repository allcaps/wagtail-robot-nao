# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 00:15
from __future__ import unicode_literals

from django.db import migrations
import home.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='description',
        ),
        migrations.AlterField(
            model_name='page',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'alignment', home.models.ImageFormatChoiceBlock())], icon='image', label='Image'))]),
        ),
    ]
