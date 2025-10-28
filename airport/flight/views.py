from django.shortcuts import render, redirect
from django.db.models import Max, F
from django.contrib import messages

from .models import Route, AirportNode
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
            
            # ✅ Automatically assign next position if not given
            if not node.position:
                last_node = AirportNode.objects.filter(route=node.route).order_by('-position').first()
                node.position = (last_node.position + 1) if last_node else 1

            node.save()
            messages.success(request, f"Node added to route {node.route.name} at position {node.position}.")
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
            current_pos = form.cleaned_data['current_position']
            n = form.cleaned_data['n']
            direction = form.cleaned_data['direction']

            # compute target position
            if direction == 'left':
                target_pos = current_pos - n
            else:
                target_pos = current_pos + n

            try:
                result = AirportNode.objects.get(route=route, position=target_pos)
            except AirportNode.DoesNotExist:
                result = None
                messages.warning(request, f"No node at position {target_pos} for route {route.name}.")
    else:
        form = NthSearchForm()
    return render(request, 'flights/search_nth.html', {'form': form, 'result': result})


def longest_nodes(request):
    """
    Shows, for each airport code present in any node, the node with the maximum duration.
    Also show the overall longest node.
    """
    # For clarity: find longest node by airport_code
    # use values + annotate
    from django.db.models import Max
    # Get distinct airport codes
    airport_codes = AirportNode.objects.values_list('airport_code', flat=True).distinct()
    longest_per_airport = []
    for code in airport_codes:
        node = AirportNode.objects.filter(airport_code=code).order_by('-duration').first()
        if node:
            longest_per_airport.append(node)

    overall_longest = AirportNode.objects.order_by('-duration').first()

    return render(request, 'flights/longest_nodes.html', {
        'longest_per_airport': longest_per_airport,
        'overall_longest': overall_longest,
    })


def shortest_between(request):
    best_result = None
    if request.method == 'POST':
        form = ShortestBetweenForm(request.POST)
        if form.is_valid():
            route_limit = form.cleaned_data['route']
            a = form.cleaned_data['airport_a'].strip().upper()
            b = form.cleaned_data['airport_b'].strip().upper()

            routes = Route.objects.all() if not route_limit else Route.objects.filter(pk=route_limit.pk)
            shortest = None
            shortest_route = None
            for route in routes:
                # get nodes for this route indexed by airport_code -> possible multiple positions (choose first/each)
                nodes = list(route.nodes.all().order_by('position'))
                # build map airport_code -> list of positions (multiple stops of same airport possible)
                pos_map = {}
                for n in nodes:
                    pos_map.setdefault(n.airport_code.upper(), []).append(n.position)

                if a in pos_map and b in pos_map:
                    # For each pair of positions, evaluate travel time
                    for pA in pos_map[a]:
                        for pB in pos_map[b]:
                            if pA == pB:
                                total = 0.0
                            else:
                                start = min(pA, pB)
                                end = max(pA, pB)
                                # sum durations for positions start .. end-1 inclusive
                                segment_nodes = [nd for nd in nodes if start <= nd.position < end]
                                total = sum(nd.duration for nd in segment_nodes)
                            if shortest is None or total < shortest:
                                shortest = total
                                shortest_route = {
                                    'route': route,
                                    'posA': pA,
                                    'posB': pB,
                                    'total': total,
                                }
            best_result = shortest_route
            if best_result is None:
                messages.warning(request, "No route contains both airports.")
    else:
        form = ShortestBetweenForm()

    return render(request, 'flights/shortest_between.html', {
        'form': form,
        'result': best_result,
    })

def route_summary(request):
    """Display each route with its total duration, start & end airports."""
    routes = Route.objects.all()
    summary = []

    for route in routes:
        nodes = route.nodes.all().order_by('position')
        if nodes.exists():
            summary.append({
                'route_name': route.name,
                'start_airport': nodes.first().airport_code,
                'end_airport': nodes.last().airport_code,
                'total_duration': route.total_duration(),
                'num_nodes': nodes.count(),
            })

    return render(request, 'flights/route_summary.html', {'summary': summary})
