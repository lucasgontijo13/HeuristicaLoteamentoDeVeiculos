import os
from model import Instance


def read_instance(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    name = None
    capacity = None
    dimension = None
    coords = {}
    demands = {}
    depot = None

    section = None

    for line in lines:
        if line.startswith("NAME"):
            name = line.split(":")[1].strip()

        elif line.startswith("CAPACITY"):
            capacity = int(line.split(":")[1].strip())

        elif line.startswith("DIMENSION"):
            dimension = int(line.split(":")[1].strip())

        elif line == "NODE_COORD_SECTION":
            section = "coords"
            continue

        elif line == "DEMAND_SECTION":
            section = "demands"
            continue

        elif line == "DEPOT_SECTION":
            section = "depot"
            continue

        elif line == "EOF":
            break

        else:
            if section == "coords":
                parts = line.split()
                if len(parts) >= 3:
                    node_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    coords[node_id] = (x, y)

            elif section == "demands":
                parts = line.split()
                if len(parts) >= 2:
                    node_id = int(parts[0])
                    demand = int(parts[1])
                    demands[node_id] = demand

            elif section == "depot":
                if line != "-1":
                    depot = int(line)

    if name is None:
        raise ValueError("NAME não encontrado na instância.")
    if capacity is None:
        raise ValueError("CAPACITY não encontrado na instância.")
    if depot is None:
        raise ValueError("DEPOT_SECTION não encontrado corretamente.")
    if not coords:
        raise ValueError("NODE_COORD_SECTION vazio ou inválido.")
    if not demands:
        raise ValueError("DEMAND_SECTION vazio ou inválido.")
    if dimension is not None and len(coords) != dimension:
        print("Aviso: quantidade de coordenadas diferente de DIMENSION.")

    return Instance(
        name=name,
        capacity=capacity,
        coords=coords,
        demands=demands,
        depot=depot
    )