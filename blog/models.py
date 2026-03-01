from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from tinymce.models import HTMLField
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import HttpResponse


class NewsAndEventsIndexPage(Page):
    parent_page_types = ['home.HomePage']
    max_count = 1
    template = 'blog/news_and_events_index_page.html'
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    # subpage_types = ['blog.NewsIndexPage', 'blog.BlogsIndexPage', 'blog.EventsIndexPage']

    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        print('news and events index page')
        # Add any custom context data here
        return context


# Index Page: NewsIndexPage
class NewsIndexPage(Page):
    parent_page_types = ['blog.NewsAndEventsIndexPage']
    # subpage_types = ['blog.NewsPage']
    max_count = 1
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    svg_icon = models.TextField(blank=True, null=True)
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
        FieldPanel('icon'),
        FieldPanel('featured_image'),
    ]


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all blog posts
        blog_posts = NewsPage.objects.child_of(self).live().order_by('-published_date')
        
        # Paginate the blog posts
        paginator = Paginator(blog_posts, 5)  # Show 6 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['posts'] = page_obj
        return context

class BlogIndex(Page):
    parent_page_types = ['home.HomePage', 'blog.NewsAndEventsIndexPage']
    # subpage_types = ['blog.BlogPage']
    max_count = 1
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    svg_icon = models.TextField(blank=True, null=True)
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
        FieldPanel('icon'),
        FieldPanel('featured_image'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all blog posts
        blog_posts = BlogPage.objects.child_of(self).live().order_by('-published_date')
        
        # Paginate the blog posts
        paginator = Paginator(blog_posts, 5)  # Show 6 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['posts'] = page_obj
        return context
    
# Index Page: EventsIndexPage
class EventsIndexPage(Page):
    parent_page_types = ['blog.NewsAndEventsIndexPage']
    # subpage_types = ['blog.EventPage']
    max_count = 1
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    svg_icon = models.TextField(blank=True, null=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
        FieldPanel('svg_icon'),
        FieldPanel('featured_image'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all blog posts
        blog_posts = EventPage.objects.child_of(self).live()
        
        # Paginate the blog posts
        paginator = Paginator(blog_posts, 10)  # Show 6 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['posts'] = page_obj
        return context

# Content Page: NewsPage
class NewsPage(Page):
    template = 'blog/partials/posts/single_post_page.html'
    parent_page_types = ['blog.NewsIndexPage']
    published_date = models.DateField()
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = HTMLField()

    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
        FieldPanel('published_date'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get the first 5 posts, ordered by published_date, excluding the current post
        recent_posts = NewsPage.objects.live().exclude(id=self.id).order_by('-published_date')[:5]
        
        # Add the custom context variable
        context['recent_posts'] = recent_posts
        context['page_type'] = 'News'
        return context
class BlogPage(Page):
    template = 'blog/partials/posts/single_post_page.html'
    parent_page_types = ['blog.BlogIndex']
    published_date = models.DateField(null=True, blank=True)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    featured_text = models.CharField(max_length=255, blank=True, null=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Featured Image'
    )
    body = HTMLField()

    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
        FieldPanel('published_date'),
        FieldPanel('featured_text'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get the first 5 posts, ordered by published_date, excluding the current post
        recent_posts = BlogPage.objects.live().exclude(id=self.id).order_by('-published_date')[:3]
        
        # Add the custom context variable
        context['recent_posts'] = recent_posts
        context['page_type'] = 'Blogs'
        return context

class EventPage(Page):
    template = 'blog/partials/posts/single_event_page.html'
    parent_page_types = ['blog.EventsIndexPage']
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    event_date = models.DateField(null=True, blank=True, verbose_name="Event Start Date")
    event_end_date = models.DateField(null=True, blank=True, verbose_name="Event End Date")
    event_time = models.CharField(max_length=200, null=True, blank=True, verbose_name="Event Start Time")
    event_end_time = models.CharField(max_length=200, null=True, blank=True, verbose_name="Event End Time")
    location = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = HTMLField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
        FieldPanel('event_date'),
        FieldPanel('event_end_date'),
        FieldPanel('event_time'),
        FieldPanel('event_end_time'),
        FieldPanel('location'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get the first 5 posts, ordered by published_date, excluding the current post
        recent_posts = EventPage.objects.live().exclude(id=self.id)[:5]
        
        # Add the custom context variable
        context['recent_posts'] = recent_posts
        context['page_type'] = 'Events'
        return context
    
