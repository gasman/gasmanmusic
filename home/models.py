from html import unescape
import re

from django.db import models
from django.utils.html import strip_tags

from wagtail.admin import panels
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        context["news"] = News.objects.all()
        return context


@register_snippet
class News(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    body = RichTextField()

    panels = [
        panels.FieldRowPanel([
            panels.FieldPanel('start_date'),
            panels.FieldPanel('end_date'),
        ]),
        panels.FieldPanel('body'),
    ]

    @property
    def date_range_string(self):
        if self.end_date is None:
            return self.start_date.strftime("%-d %b %Y")
        elif self.start_date.year != self.end_date.year:
            return "%s - %s" % (
                self.start_date.strftime("%-d %b %Y"),
                self.end_date.strftime("%-d %b %Y"),
            )
        elif self.start_date.month != self.end_date.month:
            return "%s - %s" % (
                self.start_date.strftime("%-d %b"),
                self.end_date.strftime("%-d %b %Y"),
            )
        else:
            return "%s-%s" % (
                self.start_date.strftime("%-d"),
                self.end_date.strftime("%-d %b %Y"),
            )

    def save(self, *args, **kwargs):
        self.body = re.sub(r'<p.*?>', '', self.body, count=0)
        self.body = re.sub(r'</p>', '', self.body, count=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s - %s" % (
            self.date_range_string,
            unescape(strip_tags(self.body)),
        )

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = 'news'
