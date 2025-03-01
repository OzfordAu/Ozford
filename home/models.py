from django.db import models
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from blog.models import BlogPage
from courses.models import HigherEducationCoursePage
from tinymce.models import HTMLField


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

class ImportantUrlBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    url = blocks.URLBlock()
    open_in_new_tab = blocks.BooleanBlock(required=False, default=False)


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']
    max_count = 1
    banner_carousel = StreamField(
        [
            ('banner_carousel', BannerCarouselBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    about_title = models.CharField(max_length=255, null=True, blank=True)
    about_content = RichTextField(null=True, blank=True)
    about_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='About us Image'
    )
    testimonial_title = models.CharField(max_length=255, null=True, blank=True)
    testimonial_content = RichTextField(null=True, blank=True)
    testimonial_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Testimonial Image'
    )
    important_urls = StreamField(
        [
            ('important_urls', ImportantUrlBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    # body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('banner_carousel'),
        FieldPanel('about_title'),
        FieldPanel('about_content'),
        FieldPanel('about_image'),
        FieldPanel('testimonial_title'),
        FieldPanel('testimonial_content'),
        FieldPanel('testimonial_image'),
        FieldPanel('important_urls'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blog_posts'] = BlogPage.objects.live().order_by('-published_date')[:3]
        context['pg_popular_courses'] = HigherEducationCoursePage.objects.live().filter(is_popular=True, course_type='PG')
        context['ug_popular_courses'] = HigherEducationCoursePage.objects.live().filter(is_popular=True, course_type='UG')
        return context
    
class HtmlPage(Page):
    page_title = models.CharField(max_length=255, null=True, blank=False)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    body = HTMLField()
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('body'),
    ]


class LinkBlock(blocks.StructBlock):
    link_title = blocks.CharBlock(max_length=255, blank=False, null=True)
    url = blocks.CharBlock(max_length=255, blank=False, null=True)
    open_in_new_tab = blocks.BooleanBlock(required=False, default=False)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Link Block'

class LinkPage(Page):
    page_description = RichTextField(blank=True, null=True)
    link_block = StreamField(
        [
            ('link_blocks', LinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_description'),
        FieldPanel('link_block'),
    ]

class InternationalPage(Page):
    parent_page_types = ['home.HomePage']
    max_count = 1

class DomesticPage(Page):
    parent_page_types = ['home.HomePage']
    max_count = 1

class SidebarHtmlPage(Page):
    page_title = models.CharField(max_length=255, null=True, blank=False)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    body = HTMLField()
    sidebar_links = StreamField(
        [
            ('link_blocks', LinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('body'),
        FieldPanel('sidebar_links'),
    ]