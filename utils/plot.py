import matplotlib.pyplot as plt


def plot_routes(instance, routes, output_path):
    plt.figure(figsize=(10, 8))

    depot_x, depot_y = instance.coords[instance.depot]
    plt.scatter(depot_x, depot_y, s=120, marker="s", label="Depósito")

    for idx, route in enumerate(routes, start=1):
        x_values = [depot_x]
        y_values = [depot_y]

        for node in route:
            x, y = instance.coords[node]
            x_values.append(x)
            y_values.append(y)
            plt.text(x, y, str(node), fontsize=8)

        x_values.append(depot_x)
        y_values.append(depot_y)

        plt.plot(x_values, y_values, marker="o", label=f"Rota {idx}")

    plt.title(f"{instance.name} - Rotas")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()