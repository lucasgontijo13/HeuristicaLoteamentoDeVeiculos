def clarke_wright(instance):
    depot = instance.depot

    customers = [node for node in instance.coords.keys() if node != depot]

    # rota inicial: uma rota para cada cliente
    routes = {customer: [customer] for customer in customers}
    route_load = {customer: instance.demands[customer] for customer in customers}
    customer_to_route = {customer: customer for customer in customers}

    savings = []
    for i in customers:
        for j in customers:
            if i < j:
                s = instance.distance(depot, i) + instance.distance(depot, j) - instance.distance(i, j)
                savings.append((s, i, j))

    savings.sort(reverse=True, key=lambda x: x[0])

    for saving, i, j in savings:
        route_i_id = customer_to_route[i]
        route_j_id = customer_to_route[j]

        if route_i_id == route_j_id:
            continue

        route_i = routes[route_i_id]
        route_j = routes[route_j_id]

        # só pode unir extremidades
        can_merge = False
        merged_route = None

        # casos possíveis
        if route_i[-1] == i and route_j[0] == j:
            merged_route = route_i + route_j
            can_merge = True
        elif route_i[0] == i and route_j[-1] == j:
            merged_route = route_j + route_i
            can_merge = True
        elif route_i[0] == i and route_j[0] == j:
            merged_route = list(reversed(route_i)) + route_j
            can_merge = True
        elif route_i[-1] == i and route_j[-1] == j:
            merged_route = route_i + list(reversed(route_j))
            can_merge = True

        if not can_merge:
            continue

        merged_load = route_load[route_i_id] + route_load[route_j_id]

        if merged_load > instance.capacity:
            continue

        # faz merge
        new_route_id = merged_route[0]
        routes[new_route_id] = merged_route
        route_load[new_route_id] = merged_load

        for customer in merged_route:
            customer_to_route[customer] = new_route_id

        if route_i_id in routes and route_i_id != new_route_id:
            del routes[route_i_id]
            del route_load[route_i_id]

        if route_j_id in routes and route_j_id != new_route_id:
            del routes[route_j_id]
            del route_load[route_j_id]

    return list(routes.values())