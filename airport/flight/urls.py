from django.urls import path
from . import views

app_name = 'flights'

urlpatterns = [
    path('', views.index, name='index'),

    # add node (AirportNode)
    path('add-node/', views.add_node, name='add_node'),
    path('create-route/', views.create_route, name='create_route'),

    # search nth left/right
    path('search-nth/', views.search_nth_node, name='search_nth'),

    # show longest per airport
    path('longest-nodes/', views.longest_nodes, name='longest_nodes'),

    # shortest between two airports (across routes / or within chosen route)
    path('shortest-between/', views.shortest_between, name='shortest_between'),
    
    # RRoute Summary
    path('route-summary/', views.route_summary, name='route_summary'),

]
