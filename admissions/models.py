from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from tinymce.models import HTMLField

# Create your models here.
class AdmissionIndex(Page):
    parent_page_types = ['home.HomePage', 'home.InternationalPage', 'home.DomesticPage']
    max_count = 3
    template = 'home/html_page.html'
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
    body = HTMLField(null=True, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('page_subtitle'),
        FieldPanel('banner_image'),
        FieldPanel('body'),
    ]

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['blog_posts'] = BlogPage.objects.child_of(self).live().order_by('-published_date')
    #     return context

class HighSchoolFeeBlock(blocks.StructBlock):
    program = blocks.CharBlock(max_length=255, blank=False, null=True)
    cricos = blocks.CharBlock(max_length=255, blank=False, null=True)
    tution_fee = blocks.CharBlock(max_length=255, blank=False, null=True)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'High School Fee Block'

class DomesticHigherEducationFeeBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, blank=False, null=True)
    fee = DocumentChooserBlock(required=False, verbose_name='Upload Fee File')
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Domestic Higher Education Fee Block'

class HigherEductionFeeBlock(blocks.StructBlock):
    program = blocks.CharBlock(max_length=255, blank=False, null=True)
    cricos = blocks.CharBlock(max_length=255, blank=False, null=True)
    course_duration = blocks.CharBlock(max_length=255, blank=False, null=True)
    international_tution_fee = blocks.CharBlock(max_length=255, required=False, null=True)
    domestic_tuition_fee = blocks.CharBlock(max_length=255, required=False, null=True)
    domestic_fee_help = blocks.CharBlock(max_length=255, required=False, null=True)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Higher Education Fee Block'


class AccordionBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, blank=False, null=True)
    body = blocks.RichTextBlock(null=True, blank=True)

    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Accordion Block'
        
class FeePage(Page):
    parent_page_types = ['admissions.AdmissionIndex']
    subpage_types = []
    max_count = 3
    page_title = models.CharField(max_length=255, blank=False, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    page_intro = HTMLField(null=True, blank=True)
    domestic_higher_education_course_fee = HTMLField(null=True, blank=True)
    domestic_higher_education_other_fee = HTMLField(null=True, blank=True)
    domestic_high_school_course_fee = HTMLField(null=True, blank=True)
    domestic_high_school_other_fee = HTMLField(null=True, blank=True)
    domestic_elicos_course_fee = HTMLField(null=True, blank=True)
    domestic_elicos_other_fee = HTMLField(null=True, blank=True)
    international_higher_education_course_fee = HTMLField(null=True, blank=True)
    international_higher_education_other_fee = HTMLField(null=True, blank=True)
    international_high_school_course_fee = HTMLField(null=True, blank=True)
    international_high_school_other_fee = HTMLField(null=True, blank=True)
    international_elicos_course_fee = HTMLField(null=True, blank=True)
    international_elicos_other_fee = HTMLField(null=True, blank=True)
    payment_methods = StreamField(
        [
            ('payment_methods', AccordionBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    fee_help = StreamField(
        [
            ('fee_help', AccordionBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    higher_education_payment_due_dates = HTMLField(null=True, blank=True)
    high_school_payment_due_dates = HTMLField(null=True, blank=True)
    elicos_payment_due_dates = HTMLField(null=True, blank=True)
    # elicos_fee_block = StreamField(
    #     [
    #         ('elicos_fee_block', HighSchoolFeeBlock()),
    #     ],
    #     null=True,
    #     blank=True,
    #     use_json_field=True,
    # )
    # high_school_fee_block = StreamField(
    #     [
    #         ('high_school_fee_block', HighSchoolFeeBlock()),
    #     ],
    #     null=True,
    #     blank=True,
    #     use_json_field=True,
    # )
    # higher_education_fee_block = StreamField(
    #     [
    #         ('higher_education_fee_block', HigherEductionFeeBlock()),
    #     ],
    #     null=True,
    #     blank=True,
    #     use_json_field=True,
    # )
    # domestic_higher_education_fee_block = StreamField(
    #     [
    #         ('domestic_higher_education_fee_block', DomesticHigherEducationFeeBlock()),
    #     ],
    #     null=True,
    #     blank=True,
    #     use_json_field=True,
    # )

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('page_intro'),
        FieldPanel('domestic_higher_education_course_fee'),
        FieldPanel('domestic_higher_education_other_fee'),
        FieldPanel('domestic_high_school_course_fee'),
        FieldPanel('domestic_high_school_other_fee'),
        FieldPanel('domestic_elicos_course_fee'),
        FieldPanel('domestic_elicos_other_fee'),
        FieldPanel('international_higher_education_course_fee'),
        FieldPanel('international_higher_education_other_fee'),
        FieldPanel('international_high_school_course_fee'),
        FieldPanel('international_high_school_other_fee'),
        FieldPanel('international_elicos_course_fee'),
        FieldPanel('international_elicos_other_fee'),
        FieldPanel('payment_methods'),
        FieldPanel('higher_education_payment_due_dates'),
        FieldPanel('high_school_payment_due_dates'),
        FieldPanel('elicos_payment_due_dates'),
        FieldPanel('fee_help'),
        # FieldPanel('elicos_fee_block'),
        # FieldPanel('high_school_fee_block'),
        # FieldPanel('higher_education_fee_block'),
        # FieldPanel('domestic_higher_education_fee_block'),
    ]

    class Meta:
        verbose_name = "Fee Page"

class ElicosIntakeBlock(blocks.StructBlock):
    program = blocks.CharBlock(max_length=255, blank=False, null=True)
    intake = blocks.CharBlock(max_length=255, blank=False, null=True)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Elicos Intake Block'

class HighSchoolIntakeBlock(blocks.StructBlock):
    program = blocks.CharBlock(max_length=255, blank=False, null=True)
    current_intake = blocks.CharBlock(max_length=255, blank=False, null=True)
    next_intake = blocks.CharBlock(max_length=255, blank=False, null=True)
    year_10 = blocks.BooleanBlock(required=False, default=True)
    vce_year_11 = blocks.BooleanBlock(required=False, default=True)
    vce_year_12 = blocks.BooleanBlock(required=False, default=True)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Elicos Intake Block'

class HigherEducationIntakeBlock(blocks.StructBlock):
    program = blocks.CharBlock(max_length=255, blank=False, null=True)
    current_intake = blocks.CharBlock(max_length=255, blank=False, null=True)
    next_intake = blocks.CharBlock(max_length=255, blank=False, null=True)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Elicos Intake Block'

class IntakeTitleBlock(blocks.StructBlock):
    description = blocks.CharBlock(max_length=255)
    is_title = blocks.BooleanBlock(required=False, default=False)
    class Meta:
        icon = 'user'

class IntakeBlock(blocks.StructBlock):
    title = blocks.ListBlock(IntakeTitleBlock())

    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Intake Block'

class IntakePage(Page):
    parent_page_types = ['admissions.AdmissionIndex']
    subpage_types = []
    max_count = 1
    page_title = models.CharField(max_length=255, blank=False, null=True)
    page_intro = HTMLField(null=True, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='banner_image'
    )
    elicos_intake_block = StreamField(
        [
            ('elicos_intake_block', ElicosIntakeBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    high_school_intake_block = StreamField(
        [
            ('high_school_intake_block', HighSchoolIntakeBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    higher_education_intake_block = StreamField(
        [
            ('higher_education_intake_block', HigherEducationIntakeBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    higher_education_intakes = StreamField(
        [
            ('higher_education_intakes', IntakeBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    high_school_intakes = StreamField(
        [
            ('high_school_intakes', IntakeBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    elicos_intakes = StreamField(
        [
            ('elicos_intakes', IntakeBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('banner_image'),
        FieldPanel('page_intro'),
        FieldPanel('elicos_intake_block'),
        FieldPanel('high_school_intake_block'),
        FieldPanel('higher_education_intake_block'),
        FieldPanel('higher_education_intakes'),
        FieldPanel('high_school_intakes'),
        FieldPanel('elicos_intakes'),
    ]

    class Meta:
        verbose_name = "Intake Page"


    