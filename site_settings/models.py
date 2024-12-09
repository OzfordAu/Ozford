from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField


class SiteSettings(Page):
    max_count = 1
    subpage_types = []
    # parent_page_types = ['home.HomePage']
    header_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Header Logo'
    )
    footer_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Footer Logo'
    )

    footer_note = models.CharField(max_length=255, null=True, blank=True)
    
    
    content_panels = Page.content_panels + [
        FieldPanel('header_logo'),
        FieldPanel('footer_logo'),
        FieldPanel('footer_note'),
    ]

    class Meta:
        verbose_name = "Site Settings"
        app_label = 'site_settings'