from .models import Country, City, Agent
from wagtail_modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

class CountryAdmin(ModelAdmin):
    model = Country
    menu_label = "Countries"
    menu_icon = "site"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    search_fields = ("name",)

class CityAdmin(ModelAdmin):
    model = City
    menu_label = "Cities"
    menu_icon = "site"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "country")
    search_fields = ("name", "country__name")

class AgentAdmin(ModelAdmin):
    model = Agent
    menu_label = "Agents"
    menu_icon = "site"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "city", "country")
    search_fields = ("name", "city__name", "country__name")

class AgentGroup(ModelAdminGroup):
    menu_label = "Agents"
    menu_icon = "group"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (CountryAdmin, CityAdmin, AgentAdmin)

modeladmin_register(AgentGroup)
# modeladmin_register(CityAdmin)
# modeladmin_register(AgentAdmin)

# admin.site.register(Country)
# admin.site.register(City)
# admin.site.register(Agent)
