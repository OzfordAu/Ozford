from django.db import models
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel


class BannerCarouselBlock(blocks.StructBlock):
    active = blocks.BooleanBlock(default=True, required=False)
    heading = blocks.CharBlock(blank=True, null=True)
    heading_text_color = blocks.CharBlock(max_length=50, null=True, blank=True, default="#FFFFFF", verbose_name="Text Color")
    description = blocks.CharBlock(blank=True, null=True)
    description_text_color = blocks.CharBlock(max_length=50, null=True, blank=True, default="#FFFFFF", verbose_name="Text Color")
    background_image = ImageChooserBlock(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Background Image',
    )
    image_width = blocks.ChoiceBlock(choices=[
        ('full', 'Full Width'),
        ('fit', 'Fit'),
    ], default='full')

    bg_color = blocks.CharBlock(max_length=50, null=True, blank=True, default="#FFFFFF", verbose_name="Background Color")
    btn_title = blocks.CharBlock(blank=True, null=True)
    btn_link = blocks.CharBlock(blank=True, null=True)
    btn_class = blocks.CharBlock(max_length=50, null=True, blank=True, default="btn-primary", verbose_name='Button Class', help_text="Button class for learn more button. available classes are [btn-parimary (blue), btn-danger (red), btn-success (green), btn-warning (yellow), btn-info (light blue), btn-default (grey)]")

    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Banner Coursel'


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']
    banner_carousel = StreamField(
        [
            ('banner_carousel', BannerCarouselBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('banner_carousel'),
        FieldPanel('body'),
    ]

