from django.contrib import admin
from .models import Route, FlightNode

class FlightNodeInline(admin.TabularInline):
    model = FlightNode
    extra = 1

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [FlightNodeInline]

@admin.register(FlightNode)
class FlightNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'airport_code', 'node_type', 'parent', 'duration')
    list_filter = ('route', 'airport_code', 'node_type')
    search_fields = ('airport_code', 'route__name')
