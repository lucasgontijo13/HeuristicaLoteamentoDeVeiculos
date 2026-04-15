import sys
import time
import os

from parser import read_instance
from heuristics.nearest_neighbor import nearest_neighbor
from heuristics.clarke_wright import clarke_wright
from utils.output import ensure_output_dir, save_result
from utils.plot import plot_routes


def main():
    if len(sys.argv) < 4:
        print("Uso:")
        print("python main.py <instancia.vrp> <arquivo_saida.dat> <metodo>")
        print("Exemplo:")
        print("python main.py instances/A-n32-k5.vrp resultado.dat NN")
        print("python main.py instances/A-n32-k5.vrp resultado.dat CW")
        return

    instance_file = sys.argv[1]
    output_filename = sys.argv[2]
    method = sys.argv[3].upper()

    output_dir = "output"
    ensure_output_dir(output_dir)

    instance = read_instance(instance_file)

    start_time = time.perf_counter()

    if method == "NN":
        routes = nearest_neighbor(instance)
    elif method == "CW":
        routes = clarke_wright(instance)
    else:
        print("Método inválido. Use NN ou CW.")
        return

    end_time = time.perf_counter()

    cost = instance.calculate_penalized_cost(routes)
    runtime = end_time - start_time
    gap = instance.calculate_gap(cost)

    output_path = os.path.join(output_dir, output_filename)
    plot_dir = os.path.join(output_dir, "plots")
    os.makedirs(plot_dir, exist_ok=True)

    plot_path = os.path.join(plot_dir, f"{instance.name}_{method}.png")

    save_result(
        file_path=output_path,
        instance_name=instance.name,
        method=method,
        objective=cost,
        runtime=runtime,
        gap=gap,
        vehicles=len(routes)
    )

    plot_routes(instance, routes, plot_path)

    print("Execução concluída com sucesso.")
    print(f"Instância: {instance.name}")
    print(f"Método: {method}")
    print(f"Custo total: {cost:.2f}")
    print(f"Tempo: {runtime:.6f} s")
    if gap is not None:
        print(f"Gap: {gap:.2f}%")
    else:
        print("Gap: não calculado (best known não encontrado no nome da instância)")
    print(f"Veículos usados: {len(routes)}")
    print(f"Resultado salvo em: {output_path}")
    print(f"Plot salvo em: {plot_path}")


if __name__ == "__main__":
    main()