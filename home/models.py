from django.db import models
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from blog.models import BlogPage
from courses.models import HigherEducationCoursePage
from tinymce.models import HTMLField
from wagtail.documents.blocks import DocumentChooserBlock
from sidebars.models import Sidebar


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


class AccordionBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, blank=False, null=True)
    body = blocks.RichTextBlock(null=True, blank=True)

    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Accordion Block'


# ── Testimonial Block ──────────────────────────────────────────────────────────
class TestimonialBlock(blocks.StructBlock):
    name   = blocks.CharBlock(max_length=255, label='Student Name')
    course = blocks.CharBlock(max_length=255, label='Course')
    country = blocks.CharBlock(
        max_length=255,
        label='Country Line',
        help_text="e.g. Nepal → Melbourne, AUS"
    )
    badge = blocks.CharBlock(
        max_length=255,
        label='Badge Text',
        help_text="Text shown on the image badge, e.g. Master of Professional Accounting"
    )
    quote = blocks.TextBlock(label='Quote')
    photo = ImageChooserBlock(label='Photo')

    class Meta:
        icon = 'user'
        verbose_name = 'Testimonial'
# ──────────────────────────────────────────────────────────────────────────────


# ── NEW: Course Card Block ─────────────────────────────────────────────────────
class CourseCardBlock(blocks.StructBlock):
    """
    Represents a single course card shown inside a tab on the home page.
    All fields map directly to the card UI and the modal popup.
    """
    title = blocks.CharBlock(
        max_length=255,
        label='Course Title',
        help_text="e.g. Master of Information Technology",
    )
    background_image = ImageChooserBlock(
        required=False,
        label='Card Background Image',
    )
    label = blocks.CharBlock(
        max_length=255,
        label='Modal Label',
        help_text="Shown at the top of the modal popup, e.g. 'Postgraduate · Information Technology'",
    )
    tag = blocks.CharBlock(
        max_length=255,
        label='Tag / Level & Duration',
        help_text="e.g. 'Postgraduate · 2 years'",
    )
    description = blocks.TextBlock(
        label='Short Description',
        help_text="One or two sentences shown in the modal popup.",
    )
    duration = blocks.CharBlock(
        max_length=255,
        label='Duration',
        help_text="e.g. '2 years – 4 Semesters'",
    )
    intake = blocks.CharBlock(
        max_length=255,
        label='Intake Months',
        help_text="e.g. 'March, July, November'",
    )
    url = blocks.URLBlock(
        label='Course Page URL',
        help_text="Full URL to the course detail page.",
    )

    class Meta:
        icon = 'doc-full'
        verbose_name = 'Course Card'
        label_format = '{title}'
# ──────────────────────────────────────────────────────────────────────────────


# ── NEW: Courses Tab Block ─────────────────────────────────────────────────────
class CoursesTabBlock(blocks.StructBlock):
    """
    Represents one tab in the 'Find Courses' section on the home page.
    Add as many tabs as needed via the Wagtail admin.
    """
    tab_label = blocks.CharBlock(
        max_length=100,
        label='Tab Label',
        help_text="Text shown on the tab button, e.g. 'IT' or 'Business'",
    )
    tab_slug = blocks.CharBlock(
        max_length=100,
        label='Tab Slug',
        help_text=(
            "Unique identifier used for the HTML panel id — no spaces or special characters. "
            "e.g. 'it', 'business', 'early-childhood'"
        ),
    )
    courses = blocks.StreamBlock(
        [('course', CourseCardBlock())],
        label='Course Cards',
        help_text="Add the course cards to display under this tab.",
        min_num=1,
    )

    class Meta:
        icon = 'list-ul'
        verbose_name = 'Courses Tab'
        label_format = '{tab_label}'
# ──────────────────────────────────────────────────────────────────────────────


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
    testimonials = StreamField(
        [
            ('testimonial', TestimonialBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name='Testimonial Cards',
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
    announcement_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Rolling announcement message"
    )

    show_announcement = models.BooleanField(default=True)

    # ── NEW: CMS-editable course tabs for the Find Courses section ────────────
    course_tabs = StreamField(
        [
            ('tab', CoursesTabBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name='Find Courses — Tabs',
        help_text=(
            "Each item is one tab in the 'Popular courses at Ozford' section. "
            "Add tabs for IT, Business, Accounting, Early Childhood, etc. "
            "and fill in the course cards for each tab."
        ),
    )
    # ──────────────────────────────────────────────────────────────────────────

    content_panels = Page.content_panels + [
        FieldPanel('banner_carousel'),
        FieldPanel('about_title'),
        FieldPanel('about_content'),
        FieldPanel('about_image'),
        FieldPanel('testimonial_title'),
        FieldPanel('testimonials'),        # ── NEW
        FieldPanel('important_urls'),
        FieldPanel('announcement_text'),
        FieldPanel('show_announcement'),
        # ── NEW ──
        FieldPanel('course_tabs'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blog_posts'] = BlogPage.objects.live().order_by('-published_date')[:3]
        context['pg_popular_courses'] = HigherEducationCoursePage.objects.live().filter(is_popular=True, course_type='PG')
        context['ug_popular_courses'] = HigherEducationCoursePage.objects.live().filter(is_popular=True, course_type='UG')
        context['course_tabs'] = self.course_tabs  # ← add this
        return context


class HtmlPage(Page):
    page_title = models.CharField(max_length=255, null=True, blank=False)
    page_subtitle = models.CharField(max_length=255, null=True, blank=True)
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
        FieldPanel('page_subtitle'),
        FieldPanel('banner_image'),
        FieldPanel('body'),
    ]


class LinkBlock(blocks.StructBlock):
    link_title = blocks.CharBlock(max_length=255, blank=False, null=True)
    url = blocks.CharBlock(max_length=255, blank=False, null=True)
    is_active_link = blocks.BooleanBlock(default=False, required=False)
    open_in_new_tab = blocks.BooleanBlock(required=False, default=False)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Link Block'

class LinkPage(Page):
    page_title = models.CharField(max_length=255, null=True, blank=False)
    page_subtitle = models.CharField(max_length=255, null=True, blank=True)
    link_block = StreamField(
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
        FieldPanel('link_block'),
    ]
    
SIDEBAR_TYPE = {
    ('sidebar', 'Sidebar'),
    ('sidebar_links', 'Sidebar Links'),
}
class LinkPageSidebar(Page):
    page_title = models.CharField(max_length=255, null=True, blank=False)
    page_subtitle = models.CharField(max_length=255, null=True, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    page_intro =HTMLField(null=True, blank=True)
    link_block = StreamField(
        [
            ('link_blocks', LinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    sidebar_type = models.CharField(max_length=255, choices=SIDEBAR_TYPE, default='sidebar_links', null=True, blank=True)
    sidebar_links = StreamField(
        [
            ('link_blocks', LinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    sidebar = models.ForeignKey(
        Sidebar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='sidebar'
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('page_subtitle'),
        FieldPanel('page_intro'),
        FieldPanel('sidebar_type'),
        FieldPanel('sidebar'),
        FieldPanel('link_block'),
        FieldPanel('sidebar_links'),
    ]

class InternationalPage(Page):
    parent_page_types = ['home.HomePage']
    max_count = 1

class DomesticPage(Page):
    parent_page_types = ['home.HomePage']
    max_count = 1


class SidebarHtmlPage(Page):
    page_title = models.CharField(max_length=255, null=True, blank=False)
    page_subtitle = models.CharField(max_length=255, null=True, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    body = HTMLField()
    sidebar_type = models.CharField(max_length=255, choices=SIDEBAR_TYPE, default='sidebar_links', null=True, blank=True)
    sidebar_links = StreamField(
        [
            ('link_blocks', LinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    sidebar = models.ForeignKey(
        Sidebar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='sidebar'
    )
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('page_subtitle'),
        FieldPanel('banner_image'),
        FieldPanel('sidebar_type'),
        FieldPanel('sidebar'),
        FieldPanel('body'),
        FieldPanel('sidebar_links'),
    ]


class AccordionHtmlPage(Page):
    page_title = models.CharField(max_length=255, null=True, blank=False)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    top_content = HTMLField(null=True, blank=True)
    accordion_blocks = StreamField(
        [
            ('accordion_block', AccordionBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    bottom_content = HTMLField(null=True, blank=True)
    sidebar_type = models.CharField(max_length=255, choices=SIDEBAR_TYPE, default='sidebar_links', null=True, blank=True)
    sidebar_links = StreamField(
        [
            ('link_blocks', LinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    sidebar = models.ForeignKey(
        Sidebar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='sidebar'
    )
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('sidebar_type'),
        FieldPanel('sidebar'),
        FieldPanel('top_content'),
        FieldPanel('accordion_blocks'),
        FieldPanel('bottom_content'),
        FieldPanel('sidebar_links'),
    ]

class DocumentItemBlock(blocks.StructBlock):
    DISPLAY_DOC_TYPE = {
        ('doc', 'Document'),
        ('link', 'Link'),
    }
    title = blocks.CharBlock(max_length=255)
    document = DocumentChooserBlock(required=False, max_length=255)
    link = blocks.CharBlock(max_length=255, required=False)
    display_doc_type = blocks.ChoiceBlock(choices=DISPLAY_DOC_TYPE, required=False, default='doc')
    open_in_new_tab = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = 'user'
        # template = 'blocks/team_member_block.html'

class DocumentPageSidebar(Page):
    page_title = models.CharField(max_length=255, null=True, blank=False)
    page_subtitle = models.CharField(max_length=255, null=True, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    page_intro =HTMLField(null=True, blank=True)
    document_block = StreamField(
        [
            ('document_block', DocumentItemBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    sidebar_type = models.CharField(max_length=255, choices=SIDEBAR_TYPE, default='sidebar_links', null=True, blank=True)
    sidebar_links = StreamField(
        [
            ('link_blocks', LinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    sidebar = models.ForeignKey(
        Sidebar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='sidebar'
    )
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('page_subtitle'),
        FieldPanel('sidebar_type'),
        FieldPanel('sidebar'),
        FieldPanel('page_intro'),
        FieldPanel('document_block'),
        FieldPanel('sidebar_links'),
    ]
