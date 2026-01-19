from django.shortcuts import render, redirect
from django.db.models import Max, F
from django.contrib import messages

from .models import Route, FlightNode
from .forms import AddRouteNodeForm, CreateRouteForm, NthSearchForm, ShortestBetweenForm

def index(request):
    routes = Route.objects.all()
    return render(request, 'flights/index.html', {'routes': routes})


def create_route(request):
    if request.method == 'POST':
        form = CreateRouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Route created.")
            return redirect('flights:index')
    else:
        form = CreateRouteForm()
    return render(request, 'flights/create_route.html', {'form': form})


def add_node(request):
    if request.method == 'POST':
        form = AddRouteNodeForm(request.POST)
        if form.is_valid():
            node = form.save(commit=False)
            
            if node.node_type == 'root':
                if FlightNode.objects.filter(route=node.route, node_type='root').exists():
                    messages.error(request, f"Route {node.route.name} already has a Root node.")
                    return render(request, 'flights/add_node.html', {'form': form})
                node.parent = None
            else:
                if not node.parent:
                   messages.error(request, "Non-root node must have a parent.")
                   return render(request, 'flights/add_node.html', {'form': form})
                
                if FlightNode.objects.filter(parent=node.parent, node_type=node.node_type).exists():
                    messages.error(request, f"Parent {node.parent.airport_code} already has a {node.get_node_type_display()} child.")
                    return render(request, 'flights/add_node.html', {'form': form})

            node.save()
            messages.success(request, f"Node {node.airport_code} added to route {node.route.name}.")
            return redirect('flights:index')
    else:
        form = AddRouteNodeForm()
    return render(request, 'flights/add_node.html', {'form': form})


def search_nth_node(request):
    result = None
    if request.method == 'POST':
        form = NthSearchForm(request.POST)
        if form.is_valid():
            route = form.cleaned_data['route']
            start_node = form.cleaned_data['start_node']
            n = form.cleaned_data['n']
            direction = form.cleaned_data['direction']

            current = start_node
            if not current:
                current = FlightNode.objects.filter(route=route, node_type='root').first()
            
            if not current:
                 messages.warning(request, "Route has no root node.")
            else:
                found = True
                path = [current.airport_code]
                for i in range(n):
                    try:
                        next_node = FlightNode.objects.get(parent=current, node_type=direction)
                        current = next_node
                        path.append(current.airport_code)
                    except FlightNode.DoesNotExist:
                        found = False
                        break
                
                if found:
                    result = current
                    messages.success(request, f"Found: {result.airport_code}. Path: {' -> '.join(path)}")
                else:
                    messages.warning(request, f"No node found at {n} steps {direction}.")

    else:
        form = NthSearchForm()
    return render(request, 'flights/search_nth.html', {'form': form, 'result': result})


def longest_nodes(request):
    overall_longest = FlightNode.objects.order_by('-duration').first()
    top_nodes = FlightNode.objects.order_by('-duration')[:5]

    return render(request, 'flights/longest_nodes.html', {
        'overall_longest': overall_longest,
        'top_nodes': top_nodes,
    })


def shortest_between(request):
    best_result = None
    if request.method == 'POST':
        form = ShortestBetweenForm(request.POST)
        if form.is_valid():
            route_limit = form.cleaned_data['route']
            a_code = form.cleaned_data['airport_a'].strip()
            b_code = form.cleaned_data['airport_b'].strip()

            routes = [route_limit] if route_limit else Route.objects.all()
            
            shortest_dist = None
            shortest_path_info = None

            for route in routes:
                nodes_a = list(FlightNode.objects.filter(route=route, airport_code__iexact=a_code))
                nodes_b = list(FlightNode.objects.filter(route=route, airport_code__iexact=b_code))
                
                if not nodes_a or not nodes_b:
                    continue

                for na in nodes_a:
                    for nb in nodes_b:
                        dist = calculate_tree_distance(na, nb)
                        if dist is not None:
                            if shortest_dist is None or dist < shortest_dist:
                                shortest_dist = dist
                                shortest_path_info = {
                                    'route': route,
                                    'node_a': na,
                                    'node_b': nb,
                                    'distance': dist
                                }
            
            best_result = shortest_path_info
            if not best_result:
                messages.warning(request, "No path found between these airports.")

    else:
        form = ShortestBetweenForm()

    return render(request, 'flights/shortest_between.html', {
        'form': form,
        'result': best_result,
    })

def calculate_tree_distance(node_a, node_b):
    if node_a == node_b:
        return 0.0
    
    ancestors_a = {}
    curr = node_a
    dist_from_a = 0.0
    while curr:
        ancestors_a[curr.id] = (curr, dist_from_a)
        if curr.parent:
            dist_from_a += curr.duration 
        curr = curr.parent

    curr = node_b
    dist_from_b = 0.0
    lca = None
    
    while curr:
        if curr.id in ancestors_a:
            lca = curr
            break
        if curr.parent:
            dist_from_b += curr.duration
        curr = curr.parent
    
    if lca:
        dist_a_lca = ancestors_a[lca.id][1]
        return dist_from_b + dist_a_lca
    
    return None

def route_summary(request):
    routes = Route.objects.all()
    summary = []
    for r in routes:
        root = r.nodes.filter(node_type='root').first()
        count = r.nodes.count()
        summary.append({'route': r, 'root': root, 'count': count})
    return render(request, 'flights/route_summary.html', {'summary': summary})
