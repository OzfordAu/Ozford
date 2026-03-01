from django.db import models
from wagtail import blocks
from wagtail.fields import StreamField

# Create your models here.
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

class LinkBlock(blocks.StructBlock):
    link_title = blocks.CharBlock(max_length=255, blank=False, null=True)
    url = blocks.CharBlock(max_length=255, blank=False, null=True)
    open_in_new_tab = blocks.BooleanBlock(required=False, default=False)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Link Block'

@register_snippet
class Sidebar(models.Model):
    title = models.CharField(max_length=255)
    sidebar_heading = models.CharField(max_length=255, blank=True, null=True)
    content = StreamField(
        [
            ('link_blocks', LinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("sidebar_heading"),
        FieldPanel("content"),
    ]

    def __str__(self):
        return self.title
