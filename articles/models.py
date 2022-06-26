from django.db import models
from wagtail import blocks
from wagtail.admin import panels
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.fields import StreamField

class ArticlePage(Page):
    body = StreamField([
        ("paragraph", blocks.RichTextBlock()),
        ("embed", blocks.RawHTMLBlock()),
        ("image", ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        panels.FieldPanel("body"),
    ]
