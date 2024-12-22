from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock


class BlogIndex(Page):
    parent_page_types = ['home.HomePage']
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blog_posts'] = BlogPage.objects.child_of(self).live().order_by('-published_date')
        return context


class BlogPage(Page):
    parent_page_types = ['blog.BlogIndex']
    published_date = models.DateField(null=True, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Featured Image'
    )
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('published_date'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]
