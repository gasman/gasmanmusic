from html import unescape
import json
import re

from django.db import models
from django.utils.html import strip_tags
from modelcluster.fields import ParentalKey

from wagtail.admin import panels
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet
from wagtailmedia.models import Media
from wagtailmedia.edit_handlers import MediaChooserPanel


class HomePage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        context["news"] = News.objects.all()
        context["audio_tracks_json"] = json.dumps([
            {
                "title": item.track.title,
                "file": item.track.url,
            }
            for item in self.audio_tracks.select_related('track')
        ])
        return context

    @property
    def freezer_follow_urls(self):
        urls = ['/static/images/gasman_revision2014.jpg']
        for item in self.audio_tracks.select_related('track'):
            urls.append(item.track.url)
        return urls

    content_panels = Page.content_panels + [
        panels.FieldPanel("intro"),
        panels.InlinePanel("audio_tracks", label="Audio tracks"),
    ]


class HomePageAudioTrack(Orderable):
    page = ParentalKey(HomePage, related_name="audio_tracks")
    track = models.ForeignKey(Media, on_delete=models.CASCADE)

    panels = [
        MediaChooserPanel('track'),
    ]


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
