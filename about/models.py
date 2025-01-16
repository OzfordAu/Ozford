from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import StructBlock, CharBlock, ListBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail import blocks

# Create your models here.
class AboutIndex(Page):
    parent_page_types = ['home.HomePage']
    max_count = 1

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
        FieldPanel('page_description'),
        FieldPanel('google_map'),
        FieldPanel('contact_block'),
    ]

    class Meta:
        verbose_name = "Contact Page"



class TeamMemberBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=255)
    position = blocks.CharBlock(max_length=255)
    profile_image = ImageChooserBlock()
    description = blocks.RichTextBlock()

    class Meta:
        icon = 'user'
        template = 'blocks/team_member_block.html'

class DepartmentBlock(blocks.StructBlock):
    department_title = blocks.CharBlock(max_length=255)
    team_members = blocks.ListBlock(TeamMemberBlock())

    class Meta:
        icon = 'circle-plus'
        template = 'blocks/department_block.html'
        verbose_name = 'Department'

class TeamPage(Page):
    parent_page_types = ['about.AboutIndex']
    subpage_types = []
    max_count = 1
    
    departments = StreamField(
        [
            ('department', DepartmentBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('departments'),
    ]

    