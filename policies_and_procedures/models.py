from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from tinymce.models import HTMLField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.panels import FieldPanel
from home.models import LinkBlock

class PoliciesAndProceduresIndexPage(Page):
    parent_page_types = ['home.HomePage']
    max_count = 1
    template = 'page-sidebar-right.html'
    page_title = models.CharField(max_length=255, blank=False, null=True)
    page_subtitle = models.CharField(max_length=255, blank=True, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    body = HTMLField(null=True, blank=True)
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
        FieldPanel('page_subtitle'),
        FieldPanel('banner_image'),
        FieldPanel('body'),
        FieldPanel('sidebar_links'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all blog posts
        posts = PoliciesAndProceduresSubpage.objects.child_of(self).live()
        
        context['posts'] = posts
        return context



class PolicyAndProcedureItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    DISPLAY_DOC_TYPE = {
        ('doc', 'Document'),
        ('link', 'Link'),
    }
    policy = DocumentChooserBlock(required=False)
    policy_link = blocks.URLBlock(required=False)
    procedure = DocumentChooserBlock(required=False)
    procedure_link = blocks.URLBlock(required=False)
    display_doc_type = blocks.ChoiceBlock(choices=DISPLAY_DOC_TYPE, required=False, default='doc')
    open_in_new_tab = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = 'user'
        # template = 'blocks/team_member_block.html'

class PoliciesAndProceduresBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    policy_and_procedure = blocks.ListBlock(PolicyAndProcedureItemBlock())

    class Meta:
        icon = 'circle-plus'
        # template = 'blocks/department_block.html'
        verbose_name = 'Policies and Procedures Block'


class PoliciesAndProceduresSubpage(Page):
    parent_page_types = ['policies_and_procedures.PoliciesAndProceduresIndexPage']
    page_title = models.CharField(max_length=255, blank=False, null=True)
    page_subtitle = models.CharField(max_length=255, blank=True, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    intro = HTMLField(null=True, blank=True)
    policies_and_procedures = StreamField([
        ('policies_and_procedures', PoliciesAndProceduresBlock())
    ], null=True, blank=True)

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
        FieldPanel('page_subtitle'),
        FieldPanel('banner_image'),
        FieldPanel('intro'),
        FieldPanel('policies_and_procedures'),
        FieldPanel('sidebar_links'),
    ]