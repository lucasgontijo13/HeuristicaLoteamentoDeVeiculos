import os


def ensure_output_dir(output_dir):
    os.makedirs(output_dir, exist_ok=True)


def save_result(file_path, instance_name, method, objective, runtime, gap, vehicles):
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("INSTANCE METHOD OBJECTIVE RUNTIME GAP VEHICLES\n")

        gap_str = f"{gap:.2f}" if gap is not None else "N/A"
        f.write(
            f"{instance_name} {method} {objective:.2f} {runtime:.6f} {gap_str} {vehicles}\n"
        )