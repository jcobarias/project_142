import csv
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_charts():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        RESULTS_DIR = BASE_DIR
        CSV_PATH = os.path.join(RESULTS_DIR, "memory_benchmark_results.csv")

        scales = []
        bf_mem = []
        l_mem = []
        ls_mem = []

        with open(CSV_PATH, mode="r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                scales.append(row["Scale"])

                bf_mem.append(float(row["BF_Memory"].replace(" MB", "")))
                l_mem.append(float(row["L_Memory"].replace(" MB", "")))
                ls_mem.append(float(row["LS_Memory"].replace(" MB", "")))

        plt.style.use("ggplot")

        x = np.arange(len(scales))
        width = 0.25

        plt.figure(figsize=(10, 6))

        plt.bar(x - width, bf_mem, width, label="Brute Force", color="#e74c3c")
        plt.bar(x, l_mem, width, label="L-Assignment", color="#3498db")
        plt.bar(x + width, ls_mem, width, label="L-Star Assignment", color="#2ecc71")

        plt.xlabel("Input Scale")
        plt.ylabel("Memory Usage (MB)")
        plt.title("Memory Usage Comparison")
        plt.xticks(x, scales)
        plt.legend()

        for i, val in enumerate(bf_mem):
            plt.text(i - width, val, f"{val:.2f}", ha="center", va="bottom", fontsize=8)

        for i, val in enumerate(l_mem):
            plt.text(i, val, f"{val:.2f}", ha="center", va="bottom", fontsize=8)

        for i, val in enumerate(ls_mem):
            plt.text(i + width, val, f"{val:.2f}", ha="center", va="bottom", fontsize=8)

        plt.tight_layout()

        output_path = os.path.join(RESULTS_DIR, "memory_usage_chart.png")
        plt.savefig(output_path)

        print(f"Generated: {output_path}")

    except Exception as e:
        print(f"Error generating charts: {e}")

if __name__ == "__main__":
    generate_charts()