import subprocess
import random
import re
import os
import csv

# benchmark.py - Benchmarking MSS Implementations
# This script runs the three MSS implementations against different scales of input and reports execution times.

# Define Scales
SCALES = {
    "Small Scale":  {"n": 10, "k": 3},
    "Medium Scale": {"n": 14, "k": 3},
    "Large Scale":  {"n": 16, "k": 3}
}

# Implementation Executables (relative to this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(BASE_DIR, "..", "code")
RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")

IMPLEMENTATIONS = {
    "Brute Force":       os.path.join(CODE_DIR, "brute_force.exe"),
    "L-Assignment":      os.path.join(CODE_DIR, "l_assignment.exe"),
    "L-Star Assignment": os.path.join(CODE_DIR, "l_star_ass.exe")
}

def generate_input(n, k):
    elements = [str(random.randint(1, 100)) for _ in range(n)]
    return f"{n}\n{' '.join(elements)}\n{k}"

def run_benchmark():
    # Verify executables
    for name, path in IMPLEMENTATIONS.items():
        if not os.path.exists(path):
            print(f"Error: Executable {path} not found. Please compile the C files first.")
            return

    results = []

    print("Starting Benchmarks...")
    for scale_name, params in SCALES.items():
        n, k = params["n"], params["k"]
        print(f"Testing {scale_name} (n={n}, k={k})...")
        
        input_data = generate_input(n, k)
        row = {"Scale": scale_name}
        
        for impl_name, exe_path in IMPLEMENTATIONS.items():
            print(f"  Running {impl_name}...", end=" ", flush=True)
            try:
                # Use shell=False for security, and universal_newlines=True for string I/O
                process = subprocess.run(
                    [exe_path],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=60 # 1 minute timeout per run
                )
                
                if process.returncode != 0:
                    row[impl_name] = "Error"
                    print(f"Failed (Code {process.returncode})")
                    continue

                # Parse execution time and MSS value using regex
                output_str = process.stdout
                time_match = re.search(r"Execution time: ([\d.]+) seconds", output_str)
                mss_match = re.search(r"Minimum Sum of Square: ([\d.]+)", output_str)
                
                if time_match and mss_match:
                    exec_time = float(time_match.group(1))
                    mss_val = float(mss_match.group(1))
                    
                    row[f"{impl_name} Time"] = f"{exec_time:.6f}s"
                    row[f"{impl_name} MSS"] = f"{mss_val:.2f}"
                    print(f"Done (MSS: {mss_val:.2f}, Time: {exec_time:.6f}s)")
                else:
                    row[impl_name] = "Parse Error"
                    print("Failed to parse output")
                    
            except subprocess.TimeoutExpired:
                row[impl_name] = "Timeout"
                print("Timed out")
            except Exception as e:
                row[impl_name] = "Exec Error"
                print(f"Error: {str(e)}")
        
        results.append(row)

    # Print Results Table
    print("\n--- Ground Truth Verification Matrix ---")
    header = f"{'Scale':<15} | {'Brute Force (GT)':<18} | {'L-Assignment':<18} | {'L-Star Assignment':<18}"
    print(header)
    print("-" * len(header))
    for res in results:
        bf = f"{res.get('Brute Force MSS', 'N/A')} ({res.get('Brute Force Time', 'N/A')})"
        la = f"{res.get('L-Assignment MSS', 'N/A')} ({res.get('L-Assignment Time', 'N/A')})"
        ls = f"{res.get('L-Star Assignment MSS', 'N/A')} ({res.get('L-Star Assignment Time', 'N/A')})"
        print(f"{res['Scale']:<15} | {bf:<18} | {la:<18} | {ls:<18}")

    # Export to CSV
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        
    csv_file = os.path.join(RESULTS_DIR, "benchmark_results.csv")
    fieldnames = [
        "Scale", 
        "BF_MSS", "BF_Time", 
        "L_MSS", "L_Time", 
        "LS_MSS", "LS_Time"
    ]
    
    try:
        with open(csv_file, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for res in results:
                writer.writerow({
                    "Scale": res["Scale"],
                    "BF_MSS": res.get("Brute Force MSS", "N/A"),
                    "BF_Time": res.get("Brute Force Time", "N/A"),
                    "L_MSS": res.get("L-Assignment MSS", "N/A"),
                    "L_Time": res.get("L-Assignment Time", "N/A"),
                    "LS_MSS": res.get("L-Star Assignment MSS", "N/A"),
                    "LS_Time": res.get("L-Star Assignment Time", "N/A")
                })
        print(f"\nResults successfully exported to {csv_file}")
    except Exception as e:
        print(f"\nError exporting to CSV: {str(e)}")

if __name__ == "__main__":
    run_benchmark()
    input("\nPress Enter to exit...") # Keeps terminal open if run by clicking on the file
