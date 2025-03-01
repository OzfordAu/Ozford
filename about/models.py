from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import StructBlock, CharBlock, ListBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse, parse_qs
from tinymce.models import HTMLField

# Create your models here.
class MileStonesTimeline(blocks.StructBlock):
    year = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock()

    class Meta:
        icon = 'user'
        # template = 'blocks/team_member_block.html'
class AboutIndex(Page):
    parent_page_types = ['home.HomePage']
    max_count = 1
    page_title = models.CharField(max_length=255, blank=False, null=True)
    page_subtitle = RichTextField(blank=True, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    intro = HTMLField(null=True, blank=True)
    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='intro_image'
    )
    milestones_timeline = StreamField(
        [
            ('milestones_timeline', MileStonesTimeline()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('page_subtitle'),
        FieldPanel('banner_image'),
        FieldPanel('intro'),
        FieldPanel('intro_image'),
        FieldPanel('milestones_timeline'),
    ]

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['blog_posts'] = BlogPage.objects.child_of(self).live().order_by('-published_date')
    #     return context

class ContactBlock(blocks.StructBlock):
    contact_title = blocks.CharBlock(max_length=255, blank=False, null=True)
    contact_description = blocks.RichTextBlock(blank=True, null=True)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Contact Block'

class ContactPage(Page):
    parent_page_types = ['about.AboutIndex']
    subpage_types = []
    max_count = 1
    page_title = models.CharField(max_length=255, blank=False, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    page_description = RichTextField(blank=True, null=True)
    google_map = models.CharField(max_length=255, blank=False, null=True)
    contact_block = StreamField(
        [
            ('contact_blocks', ContactBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('page_description'),
        FieldPanel('google_map'),
        FieldPanel('contact_block'),
    ]

    class Meta:
        verbose_name = "Contact Page"



class TeamMemberBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=255)
    position = blocks.RichTextBlock(required=False)
    qualification = blocks.RichTextBlock(required=False)
    profile_image = ImageChooserBlock(required=False)
    description = blocks.RichTextBlock(required=False)

    class Meta:
        icon = 'user'
        # template = 'blocks/team_member_block.html'

class DepartmentBlock(blocks.StructBlock):
    department_title = blocks.CharBlock(max_length=255)
    team_members = blocks.ListBlock(TeamMemberBlock())

    class Meta:
        icon = 'circle-plus'
        # template = 'blocks/department_block.html'
        verbose_name = 'Department'

class TeamPage(Page):
    parent_page_types = ['about.AboutIndex']
    subpage_types = []
    max_count = 1
    page_title = models.CharField(max_length=255, blank=False, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    higher_education_team = StreamField(
        [
            ('higher_education_team', DepartmentBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    high_school_team = StreamField(
        [
            ('high_school_team', DepartmentBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('higher_education_team'),
        FieldPanel('high_school_team'),
    ]

# Define reusable blocks for Photo and Video
class GalleryPhotoBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False, max_length=255)
    is_active = blocks.BooleanBlock(default=True)

    class Meta:
        icon = 'image'

class GalleryVideoBlock(blocks.StructBlock):
    video_url = blocks.URLBlock(required=True, help_text='Enter the URL of the YouTube video')
    title = blocks.CharBlock(max_length=255, required=False)
    is_active = blocks.BooleanBlock(default=True)

    class Meta:
        icon = 'media'

# Unified Gallery Page
def youtube_id(url):
    """Extract YouTube video ID from URL"""
    parsed = urlparse(url)
    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    if parsed.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed.path == '/watch':
            return parse_qs(parsed.query)['v'][0]
    return ''
class GalleryIndexPage(Page):
    parent_page_types = ['about.AboutIndex']
    subpage_types = []
    max_count = 1
    page_title = models.CharField(max_length=255, blank=False, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Banner Image'
    )
    gallery_items = StreamField(
        [
            ('photo', GalleryPhotoBlock()),
            ('video', GalleryVideoBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    created_on = models.DateTimeField(auto_now_add=True)

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('gallery_items'),
    ]

   

    def get_context(self, request):
        context = super().get_context(request)
        gallery_items = [
            {
                "type": block.block_type,
                "data": {
                    **block.value,
                    # Transform to embed URL
                    "embed_url": youtube_id(block.value["video_url"])
                } if block.block_type == "video" else block.value,
                "created_on": block.value.get("created_on", None),
            }
            for block in self.gallery_items
        ]

        # Sort gallery items by created_on
        gallery_items = sorted(gallery_items, key=lambda x: x['created_on'] or '', reverse=True)
        context["gallery_items"] = gallery_items
        return context


class StoriesIndexPage(Page):
    parent_page_types = ['about.AboutIndex']
    subpage_types = []
    max_count = 1
    page_title = models.CharField(max_length=255, blank=False, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Banner Image'
    )
    gallery_items = StreamField(
        [
            ('video', GalleryVideoBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    created_on = models.DateTimeField(auto_now_add=True)

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('gallery_items'),
    ]

   

    def get_context(self, request):
        context = super().get_context(request)
        gallery_items = [
            {
                "type": block.block_type,
                "data": {
                    **block.value,
                    # Transform to embed URL
                    "embed_url": youtube_id(block.value["video_url"])
                } if block.block_type == "video" else block.value,
                "created_on": block.value.get("created_on", None),
            }
            for block in self.gallery_items
        ]

        # Sort gallery items by created_on
        gallery_items = sorted(gallery_items, key=lambda x: x['created_on'] or '', reverse=True)
        context["gallery_items"] = gallery_items
        return context

class TestimonialBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=255)
    country = blocks.CharBlock(max_length=255)
    course = blocks.CharBlock(max_length=255)
    profile_image = ImageChooserBlock(required=False)
    description = blocks.RichTextBlock(required=False)

    class Meta:
        icon = 'user'
        # template = 'blocks/team_member_block.html'

class TestimonialPage(Page):
    parent_page_types = ['about.AboutIndex']
    subpage_types = []
    max_count = 1
    page_title = models.CharField(max_length=255, blank=False, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    testimonial = StreamField(
        [
            ('testimonial', TestimonialBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('testimonial'),
    ]

