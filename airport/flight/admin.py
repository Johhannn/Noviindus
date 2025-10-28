from django.contrib import admin
from .models import Route, AirportNode

class AirportNodeInline(admin.TabularInline):
    model = AirportNode
    extra = 1

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [AirportNodeInline]

@admin.register(AirportNode)
class AirportNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'airport_code', 'position', 'duration')
    list_filter = ('route', 'airport_code')
    search_fields = ('airport_code', 'route__name')
