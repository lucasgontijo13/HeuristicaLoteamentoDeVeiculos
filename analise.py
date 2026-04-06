import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

INPUT_FILE = os.path.join("output", "resultado.dat")
OUTPUT_DIR = os.path.join("output", "analytics")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv(INPUT_FILE, sep=r"\s+")

    # converter runtime para ms
    df["RUNTIME"] = df["RUNTIME"] * 1000

    df["GAP"] = pd.to_numeric(df["GAP"], errors="coerce")
    return df


def save_runtime_bar_chart(df):
    pivot = df.pivot(index="INSTANCE", columns="METHOD", values="RUNTIME")

    ax = pivot.plot(kind="bar", figsize=(14, 7))
    ax.set_title("Tempo de execução por instância")
    ax.set_xlabel("Instância")
    ax.set_ylabel("Runtime (ms)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "grafico_runtime_barras.png"))
    plt.close()


def save_gap_boxplot(df):
    gap_nn = df[df["METHOD"] == "NN"]["GAP"].dropna()
    gap_cw = df[df["METHOD"] == "CW"]["GAP"].dropna()

    plt.figure(figsize=(8, 6))
    plt.boxplot([gap_nn, gap_cw], tick_labels=["NN", "CW"])
    plt.title("Boxplot dos gaps por heurística")
    plt.ylabel("Gap (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "boxplot_gaps.png"))
    plt.close()


def confidence_interval_95(values):
    values = values.dropna()
    n = len(values)

    if n < 2:
        return None, None, None

    mean = values.mean()
    std = values.std(ddof=1)
    t_value = stats.t.ppf(0.975, df=n - 1)
    margin = t_value * (std / (n ** 0.5))

    lower = mean - margin
    upper = mean + margin
    return mean, lower, upper


def save_confidence_interval_table(df):
    rows = []

    for method in sorted(df["METHOD"].unique()):
        values = df[df["METHOD"] == method]["GAP"]
        result = confidence_interval_95(values)

        if result[0] is None:
            rows.append({
                "METHOD": method,
                "MEAN_GAP": None,
                "CI95_LOWER": None,
                "CI95_UPPER": None
            })
        else:
            mean, lower, upper = result
            rows.append({
                "METHOD": method,
                "MEAN_GAP": round(mean, 2),
                "CI95_LOWER": round(lower, 2),
                "CI95_UPPER": round(upper, 2)
            })

    ci_df = pd.DataFrame(rows)
    ci_df.to_csv(os.path.join(OUTPUT_DIR, "intervalo_confianca_95.csv"), index=False)

    print("\nIntervalo de confiança de 95%:")
    print(ci_df.to_string(index=False))


def main():
    df = load_data()
    save_runtime_bar_chart(df)
    save_gap_boxplot(df)
    save_confidence_interval_table(df)
    print("\nArquivos gerados em output/analytics/")


if __name__ == "__main__":
    main()