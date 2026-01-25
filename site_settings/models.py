from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class LinkBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, blank=False, null=True)
    url = blocks.CharBlock(max_length=255, blank=False, null=True)
    open_in_new_tab = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Link Block'


class SocialMediaLinkBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    # icon = ImageChooserBlock()
    icon_svg = blocks.TextBlock(null=True, required=False)
    url = blocks.CharBlock(max_length=255, blank=False, null=True)
    open_in_new_tab = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Social Media Link Block'


class SocialMediaBlock(blocks.StructBlock):
    social_media = blocks.ListBlock(SocialMediaLinkBlock())

    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Social Media'


class FooterLinkBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    links = blocks.ListBlock(LinkBlock())

    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Footer Link'

class AffiliationLogoBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    is_active = blocks.BooleanBlock(default=True, required=False)
    class Meta:
        icon = 'image'


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

    site_popup_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Site Popup Image'
    )
    popup_width = models.CharField(max_length=255, null=True, blank=True, default='300px', verbose_name="Width")
    popup_height = models.CharField(max_length=255, null=True, blank=True, default='500px', verbose_name = "Height")
    popup_class = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name="Custom Class")
    popup_start_date = models.DateField(null=True, blank=True, verbose_name='Popup Start Date')
    popup_end_date = models.DateField(null=True, blank=True, verbose_name='Popup End Date')
    popup_is_active = models.BooleanField(default=True, verbose_name='Popup is Active')

    # Rolling Message Fields
    rolling_message = models.CharField(max_length=500, null=True, blank=True, verbose_name='Rolling Message Text')
    rolling_message_is_active = models.BooleanField(default=False, verbose_name='Show Rolling Message')

    address = RichTextField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    office_hour = models.CharField(max_length=255, null=True, blank=True)
    google_map = models.CharField(max_length=255, null=True, blank=True)
    affiliations = StreamField(
        [
            ('logos', AffiliationLogoBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    footer_primary_links = StreamField(
        [
            ('footer_primary_links', FooterLinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    footer_secondary_links = StreamField(
        [
            ('footer_secondary_links', LinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    footer_social_media = StreamField(
        [
            ('footer_social_media', SocialMediaBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    acknowledgement_of_country_title = models.CharField(
        max_length=255, null=True, blank=True)
    acknowledgement_of_country_content = RichTextField(null=True, blank=True)
    copyright_content = models.TextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        # Logos
        MultiFieldPanel([
            FieldPanel('header_logo'),
            FieldPanel('footer_logo'),
        ], heading='Logos'),

        MultiFieldPanel([
            FieldPanel('site_popup_image'),
            FieldPanel('popup_width'),
            FieldPanel('popup_height'),
            FieldPanel('popup_class'),
            FieldPanel('popup_start_date'),
            FieldPanel('popup_end_date'),
            FieldPanel('popup_is_active'),
        ], heading='Site Popup Message'),

        # Rolling Message Banner
        MultiFieldPanel([
            FieldPanel('rolling_message'),
            FieldPanel('rolling_message_is_active'),
        ], heading='Rolling Message Banner'),

        # Contact Details
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('office_hour'),
            FieldPanel('phone'),
            FieldPanel('email'),
            FieldPanel('google_map'),
        ], heading='Contact Details'),

        # Footer
        MultiFieldPanel([
            # Links
                FieldPanel('affiliations'),
                FieldPanel('footer_primary_links'),
                FieldPanel('footer_secondary_links'),
                FieldPanel('footer_social_media'),
                FieldPanel('acknowledgement_of_country_title'),
                FieldPanel('acknowledgement_of_country_content'),
                FieldPanel('copyright_content'),

        ], heading='Footer Content'),
       
    ]

    class Meta:
        verbose_name = "Global Site Settings"
        app_label = 'site_settings'
