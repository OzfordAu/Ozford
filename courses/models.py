from django.db import models
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.documents import get_document_model
from wagtail.models import Page
from wagtail import blocks
from tinymce.models import HTMLField

class CoursesIndexPage(Page):
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['courses.DegreeIndexPage']
    page_title = models.CharField(max_length=255, null=True, blank=True)
    page_description = RichTextField(null=True, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Banner Image'
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('page_description'),
        FieldPanel('banner_image'),
    ]


    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context['degrees'] = DegreeIndexPage.objects.child_of(self).live()

        return context

    class Meta:
        verbose_name = 'Courses Index Page'

class DegreeIndexPage(Page):
    # max_count = 1
    parent_page_types = ['courses.CoursesIndexPage']
    subpage_types = ['courses.HigherEducationCoursePage', 'courses.HighSchoolCoursePage', 'courses.ElicosCoursePage']
    page_title = models.CharField(max_length=255, null=True, blank=True)
    page_description = RichTextField(null=True, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Banner Image'
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('page_description'),
        FieldPanel('banner_image'),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Filter courses that are direct children of this DegreeIndexPage
        context['higher_education_courses'] = HigherEducationCoursePage.objects.live().child_of(self)
        return context
    

HE_DEGREE_TYPE_CHOICES = (
    ('PG', 'Postgraduate'),
    ('UG', 'Undergraduate'),
    ('DIP', 'Diploma'),
)

class UnitBlock(blocks.StructBlock):
    unit_title = blocks.CharBlock(max_length=255, null=True)
    unit_description = blocks.RichTextBlock(null=True, required=False)
    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Unit'

class CourseUnitBlock(blocks.StructBlock):
    display_as_dropdown = blocks.BooleanBlock(default=True, help_text="If false, only course title will be displayed as lists")
    title = blocks.CharBlock(max_length=255)
    sub_title = blocks.CharBlock(max_length=255, null=True, required=False)
    units = blocks.ListBlock(UnitBlock())

    class Meta:
        icon = 'circle-plus'
        verbose_name = 'Course Unit'

class HigherEducationCoursePage(Page):
    parent_page_types = ['courses.DegreeIndexPage']
    subpage_types = []
    is_popular = models.BooleanField(default=False)
    course_type = models.CharField(max_length=3, choices=HE_DEGREE_TYPE_CHOICES, default='UG')
    course_title = models.CharField(max_length=255, null=True, blank=True)
    course_header_description = RichTextField(null=True, blank=True)
    course_brochure = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    accreditation_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Course Accreditation Logo'
    )
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Banner Image'
    )
    cricos_code = models.CharField(max_length=10, null=True, blank=True)
    study_mode = RichTextField(null=True, blank=True)
    course_duration = RichTextField(null=True, blank=True)
    intakes = RichTextField(null=True, blank=True)
    ielts_domestic = RichTextField(null=True, blank=True)
    ielts_international = RichTextField(null=True, blank=True)
    aqf_level = models.CharField(max_length=255, null=True, blank=True)
    fee_domestic = RichTextField(null=True, blank=True)
    fee_international = RichTextField(null=True, blank=True)
    course_location = RichTextField(null=True, blank=True)
    course_requirement_domestic = HTMLField(null=True, blank=True)
    course_requirement_international = HTMLField(null=True, blank=True)
    academic_requirement_domestic = HTMLField(null=True, blank=True)
    academic_requirement_international = HTMLField(null=True, blank=True)
    english_requirement_domestic = HTMLField(null=True, blank=True)
    english_requirement_international = HTMLField(null=True, blank=True)
    age_requirement_domestic = HTMLField(null=True, blank=True)
    age_requirement_international = HTMLField(null=True, blank=True)
    career_outcomes = HTMLField(null=True, blank=True)
    course_overview = HTMLField(null=True, blank=True)
    core_units_title = models.CharField(max_length=255, null=True, blank=True)
    core_units = StreamField(
        [
            ('core_units', UnitBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    course_units = StreamField(
        [
            ('course_units', CourseUnitBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    core_units_block = HTMLField(null=True, blank=True, help_text='Use this block when you only want to add title of units. This is helpful when you don\'t want to display accordions for unit title and description.')
    management_specialisation_units_title = models.CharField(max_length=255, null=True, blank=True)
    management_specialisation_units = StreamField(
        [
            ('management_specialisation_units', UnitBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    marketing_specialisation_units_title = models.CharField(max_length=255, null=True, blank=True)
    marketing_specialisation_units = StreamField(
        [
            ('marketing_specialisation_units', UnitBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    accounting_specialisation_units_title = models.CharField(max_length=255, null=True, blank=True)
    accounting_specialisation_units = StreamField(
        [
            ('accounting_specialisation_units', UnitBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    ellective_units_title = models.CharField(max_length=255, null=True, blank=True)
    ellective_units = StreamField(
        [
            ('ellective_units', UnitBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    student_workload = HTMLField(null=True, blank=True)
    pathways = HTMLField(null=True, blank=True)
    assessment_methods = HTMLField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('is_popular'),
        FieldPanel('course_type'),
        FieldPanel('course_title'),
        FieldPanel('course_header_description'),
        FieldPanel('banner_image'),
        FieldPanel('course_brochure'),
        FieldPanel('cricos_code'),
        FieldPanel('accreditation_logo'),
        MultiFieldPanel([
            FieldPanel('intakes'),
            FieldPanel('ielts_domestic'),
            FieldPanel('ielts_international'),
            FieldPanel('aqf_level'),
            FieldPanel('fee_domestic'),
            FieldPanel('fee_international'),
            FieldPanel('study_mode'),
            FieldPanel('course_duration'),
            FieldPanel('course_location'),
        ], heading='Key Facts'),

         MultiFieldPanel([
           FieldPanel('course_requirement_domestic'),
            FieldPanel('course_requirement_international'),
        ], heading='Course Requirements'),
        MultiFieldPanel([
           FieldPanel('academic_requirement_domestic'),
            FieldPanel('academic_requirement_international'),
        ], heading='Academic Requirements'),

        MultiFieldPanel([
            FieldPanel('english_requirement_domestic'),
            FieldPanel('english_requirement_international'),
        ], heading='English Language Requirements'),

        MultiFieldPanel([
            FieldPanel('age_requirement_domestic'),
            FieldPanel('age_requirement_international'),
        ], heading='Age Requirements'),

        MultiFieldPanel([
            FieldPanel('course_overview'),
            FieldPanel('course_units'),
            FieldPanel('career_outcomes'),
            FieldPanel('student_workload'),
            FieldPanel('pathways'),
            FieldPanel('assessment_methods'),
        ], heading='Course Details'),
        
        
        
        
        # FieldPanel('course_units'),
        # FieldPanel('core_units_title'),
        # FieldPanel('core_units'),
        # FieldPanel('management_specialisation_units_title'),
        # FieldPanel('management_specialisation_units'),
        # FieldPanel('marketing_specialisation_units_title'),
        # FieldPanel('marketing_specialisation_units'),
        # FieldPanel('accounting_specialisation_units_title'),
        # FieldPanel('accounting_specialisation_units'),
        # FieldPanel('ellective_units'),
        # FieldPanel('core_units_block'),
        # FieldPanel('student_workload'),
        # FieldPanel('pathways'),
        # FieldPanel('assessment_methods'),
    ]

    class Meta:
        verbose_name = "Higher Education Course Page"


class HighSchoolCoursePage(Page):
    parent_page_types = ['courses.DegreeIndexPage']
    subpage_types = []
    is_popular = models.BooleanField(default=False)
    course_title = models.CharField(max_length=255, null=True, blank=True)
    cricos_code = models.CharField(max_length=10, null=True, blank=True)
    course_header_description = RichTextField(null=True, blank=True)
    course_brochure = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Banner Image'
    )
    body = HTMLField(null=True, blank=True)
    

    content_panels = Page.content_panels + [
        FieldPanel('is_popular'),
        FieldPanel('course_title'),
        FieldPanel('cricos_code'),
        FieldPanel('course_header_description'),
        FieldPanel('course_brochure'),
        FieldPanel('banner_image'),
        FieldPanel('body'), 
       
    ]

    class Meta:
        verbose_name = "High School Course Page"


class ElicosCoursePage(Page):
    parent_page_types = ['courses.DegreeIndexPage']
    subpage_types = []
    is_popular = models.BooleanField(default=False)
    course_title = models.CharField(max_length=255, null=True, blank=True)
    cricos_code = models.CharField(max_length=10, null=True, blank=True)
    course_header_description = RichTextField(null=True, blank=True)
    course_duration = RichTextField(null=True, blank=True)
    class_hours = RichTextField(null=True, blank=True)
    location = RichTextField(null=True, blank=True)
    average_class_size = RichTextField(null=True, blank=True)
    level_available = RichTextField(null=True, blank=True)
    entry_requirements = RichTextField(null=True, blank=True)
    intakes = RichTextField(null=True, blank=True)
    fees = RichTextField(null=True, blank=True)
    course_brochure = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Banner Image'
    )
    course_overview = RichTextField(null=True, blank=True)
    learning_outcome = HTMLField(null=True, blank=True)
    assessment = RichTextField(null=True, blank=True)
    

    content_panels = Page.content_panels + [
        FieldPanel('is_popular'),
        FieldPanel('course_title'),
        FieldPanel('cricos_code'),
        FieldPanel('course_header_description'),
        FieldPanel('course_duration'),
        FieldPanel('class_hours'),
        FieldPanel('location'),
        FieldPanel('average_class_size'),
        FieldPanel('level_available'),
        FieldPanel('entry_requirements'),
        FieldPanel('intakes'),
        FieldPanel('fees'),
        FieldPanel('course_brochure'),
        FieldPanel('banner_image'),
        FieldPanel('course_overview'), 
        FieldPanel('learning_outcome'), 
        FieldPanel('assessment'), 
       
    ]

    class Meta:
        verbose_name = "Elicos Course Page"
