from __future__ import absolute_import, unicode_literals

from django import forms
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import (
    FieldBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page as BasePage
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index


class ImageBlock(StructBlock):
    image = ImageChooserBlock()

    class Meta:
        template = 'home/blocks/image_block.html'


class webappStreamBlock(StreamBlock):
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    image = ImageBlock(label="Image", icon="image")


class Page(BasePage):
    body = StreamField(webappStreamBlock())
    search_fields = BasePage.search_fields + [
        index.SearchField('body'),
    ]

Page.content_panels = [
    FieldPanel('title', classname="full title"),
    StreamFieldPanel('body'),
]
