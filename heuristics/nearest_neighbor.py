def nearest_neighbor(instance):
    unvisited = set(instance.coords.keys())
    unvisited.remove(instance.depot)

    routes = []

    while unvisited:
        route = []
        current = instance.depot
        current_load = 0

        while True:
            best_node = None
            best_distance = float("inf")

            for node in unvisited:
                demand = instance.demands[node]

                if current_load + demand > instance.capacity:
                    continue

                dist = instance.distance(current, node)
                if dist < best_distance:
                    best_distance = dist
                    best_node = node

            if best_node is None:
                break

            route.append(best_node)
            current_load += instance.demands[best_node]
            current = best_node
            unvisited.remove(best_node)

        routes.append(route)

    return routes