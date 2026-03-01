from wagtail.models import Page
from django.db import models
from wagtail.admin.panels import FieldPanel

# Country Model
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# City Model
class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.name}, {self.country.name}"

# Agent Model
class Agent(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="agents")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="agents")
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# Wagtail Page Model for Listing Agents
class AgentsIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        country_id = request.GET.get("country")
        city_id = request.GET.get("city")

        agents = Agent.objects.all()

        if country_id:
            agents = agents.filter(country_id=country_id)

        if city_id:
            agents = agents.filter(city_id=city_id)

        context["agents"] = agents
        context["countries"] = Country.objects.all()
        context["cities"] = City.objects.filter(country_id=country_id) if country_id else []

        return context
