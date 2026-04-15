import os
import subprocess

INSTANCES = [
    "A-n80-k10.vrp",
    "F-n72-k4.vrp",
    "E-n101-k14.vrp",
    "F-n135-k7.vrp",
    "M-n151-k12.vrp",
    "Golden_18.vrp",
    "CMT10.vrp",
    "Tai150b.vrp",
    "Tai385.vrp",
    "Golden_3.vrp",
    "Li_21.vrp",
    "X-n502-k39.vrp",
    "Loggi-n601-k42.vrp",
    "XL-n1701-k562.vrp",
    "XL-n2541-k121.vrp",
]



METHODS = ["NN", "CW"]

INSTANCE_DIR = "instances"
OUTPUT_FILE = "resultado.dat"


def main():
    output_path = os.path.join("output", OUTPUT_FILE)

    if os.path.exists(output_path):
        os.remove(output_path)

    for instance in INSTANCES:
        instance_path = os.path.join(INSTANCE_DIR, instance)

        if not os.path.exists(instance_path):
            print(f"[ERRO] Instância não encontrada: {instance_path}")
            continue

        for method in METHODS:
            print(f"Rodando {instance} com {method}...")
            subprocess.run(
                ["python", "main.py", instance_path, OUTPUT_FILE, method],
                check=True
            )

    print("\nExecutando análise...")
    subprocess.run(["python", "analise.py"], check=True)

    print("\nBenchmark finalizado.")
    print(f"Resultados salvos em: output/{OUTPUT_FILE}")
    print("Análises salvas em: output/analytics/")


if __name__ == "__main__":
    main()