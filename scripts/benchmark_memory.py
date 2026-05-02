import subprocess
import random
import re
import os
import csv
import platform

SCALES = {
    "Small Scale":  {"n": 10, "k": 3},
    "Medium Scale": {"n": 14, "k": 3},
    "Large Scale":  {"n": 16, "k": 3}
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = BASE_DIR
RESULTS_DIR = BASE_DIR

IMPLEMENTATIONS = {
    "Brute Force": os.path.join(CODE_DIR, "brute_force"),
    "L-Assignment": os.path.join(CODE_DIR, "l_assignment"),
    "L-Star Assignment": os.path.join(CODE_DIR, "l_star_assignment")
}

def generate_input(n, k):
    elements = [str(random.randint(1, 100)) for _ in range(n)]
    return f"{n}\n{' '.join(elements)}\n{k}\n"

def run_with_memory(exe_path, input_data):
    system_name = platform.system()

    if system_name == "Darwin":
        command = ["/usr/bin/time", "-l", exe_path]
        memory_pattern = r"(\d+)\s+maximum resident set size"
    elif system_name == "Linux":
        command = ["/usr/bin/time", "-v", exe_path]
        memory_pattern = r"Maximum resident set size \(kbytes\):\s+(\d+)"
    else:
        raise Exception("Unsupported OS. Use macOS or Linux.")

    process = subprocess.run(
        command,
        input=input_data,
        capture_output=True,
        text=True,
        timeout=60
    )

    combined_output = process.stdout + process.stderr

    mss_match = re.search(r"Minimum Sum of Square:\s+([\d.]+)", combined_output)
    memory_match = re.search(memory_pattern, combined_output)

    if not memory_match:
        return "Parse Error", "Parse Error"

    memory_value = int(memory_match.group(1))

    if system_name == "Darwin":
        memory_kb = memory_value / 1024
    else:
        memory_kb = memory_value

    memory_mb = memory_kb / 1024
    mss_value = mss_match.group(1) if mss_match else "N/A"

    return mss_value, memory_mb

def run_benchmark():
    for name, path in IMPLEMENTATIONS.items():
        if not os.path.exists(path):
            print(f"Error: Executable {path} not found. Please compile first.")
            return

    results = []

    print("Starting Memory Benchmarks...")

    for scale_name, params in SCALES.items():
        n, k = params["n"], params["k"]
        print(f"\nTesting {scale_name} (n={n}, k={k})...")

        input_data = generate_input(n, k)
        row = {"Scale": scale_name}

        for impl_name, exe_path in IMPLEMENTATIONS.items():
            print(f"  Running {impl_name}...", end=" ", flush=True)

            try:
                mss_value, memory_mb = run_with_memory(exe_path, input_data)

                row[f"{impl_name} MSS"] = mss_value

                if isinstance(memory_mb, float):
                    row[f"{impl_name} Memory"] = f"{memory_mb:.4f} MB"
                    print(f"Done (MSS: {mss_value}, Memory: {memory_mb:.4f} MB)")
                else:
                    row[f"{impl_name} Memory"] = memory_mb
                    print("Failed to parse memory")

            except subprocess.TimeoutExpired:
                row[f"{impl_name} MSS"] = "Timeout"
                row[f"{impl_name} Memory"] = "Timeout"
                print("Timed out")

            except Exception as e:
                row[f"{impl_name} MSS"] = "Error"
                row[f"{impl_name} Memory"] = "Error"
                print(f"Error: {str(e)}")

        results.append(row)

    print("\n--- Memory Usage Benchmark Matrix ---")
    header = f"{'Scale':<15} | {'Brute Force':<25} | {'L-Assignment':<25} | {'L-Star Assignment':<25}"
    print(header)
    print("-" * len(header))

    for res in results:
        bf = f"{res.get('Brute Force MSS', 'N/A')} ({res.get('Brute Force Memory', 'N/A')})"
        la = f"{res.get('L-Assignment MSS', 'N/A')} ({res.get('L-Assignment Memory', 'N/A')})"
        ls = f"{res.get('L-Star Assignment MSS', 'N/A')} ({res.get('L-Star Assignment Memory', 'N/A')})"

        print(f"{res['Scale']:<15} | {bf:<25} | {la:<25} | {ls:<25}")

    csv_file = os.path.join(RESULTS_DIR, "memory_benchmark_results.csv")

    fieldnames = [
        "Scale",
        "BF_MSS", "BF_Memory",
        "L_MSS", "L_Memory",
        "LS_MSS", "LS_Memory"
    ]

    with open(csv_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for res in results:
            writer.writerow({
                "Scale": res["Scale"],
                "BF_MSS": res.get("Brute Force MSS", "N/A"),
                "BF_Memory": res.get("Brute Force Memory", "N/A"),
                "L_MSS": res.get("L-Assignment MSS", "N/A"),
                "L_Memory": res.get("L-Assignment Memory", "N/A"),
                "LS_MSS": res.get("L-Star Assignment MSS", "N/A"),
                "LS_Memory": res.get("L-Star Assignment Memory", "N/A")
            })

    print(f"\nResults successfully exported to {csv_file}")

if __name__ == "__main__":
    run_benchmark()
    input("\nPress Enter to exit...")