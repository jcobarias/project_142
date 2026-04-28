import csv
import matplotlib.pyplot as plt
import numpy as np
import os

# generate_charts.py - Generates comparison charts from benchmark_results.csv (No Pandas version)

def generate_charts():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")
        CSV_PATH = os.path.join(RESULTS_DIR, "benchmark_results.csv")

        scales = []
        bf_mss, bf_time = [], []
        l_mss, l_time = [], []
        ls_mss, ls_time = [] , []

        with open(CSV_PATH, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                scales.append(row['Scale'])
                bf_mss.append(float(row['BF_MSS']))
                bf_time.append(float(row['BF_Time'].replace('s', '')))
                l_mss.append(float(row['L_MSS']))
                l_time.append(float(row['L_Time'].replace('s', '')))
                ls_mss.append(float(row['LS_MSS']))
                ls_time.append(float(row['LS_Time'].replace('s', '')))

        # Setting style
        plt.style.use('ggplot')
        
        # --- 1. Execution Time Chart (Log Scale) ---
        plt.figure(figsize=(10, 6))
        
        x = np.arange(len(scales))
        width = 0.25
        
        plt.bar(x - width, bf_time, width, label='Brute Force', color='#e74c3c')
        plt.bar(x, l_time, width, label='L-Assignment', color='#3498db')
        plt.bar(x + width, ls_time, width, label='L-Star Assignment', color='#2ecc71')
        
        plt.yscale('log')
        plt.xlabel('Input Scale')
        plt.ylabel('Execution Time (seconds) - Log Scale')
        plt.title('Execution Time Comparison (Log Scale)')
        plt.xticks(x, scales)
        plt.legend()
        
        plt.tight_layout()
        output_time = os.path.join(RESULTS_DIR, 'execution_time_chart.png')
        plt.savefig(output_time)
        print(f"Generated: {output_time}")

        # --- 2. MSS Value Accuracy Chart ---
        plt.figure(figsize=(10, 6))
        
        plt.bar(x - width, bf_mss, width, label='Brute Force (Optimal)', color='#e74c3c')
        plt.bar(x, l_mss, width, label='L-Assignment', color='#3498db')
        plt.bar(x + width, ls_mss, width, label='L-Star Assignment', color='#2ecc71')
        
        plt.xlabel('Input Scale')
        plt.ylabel('Minimum Sum of Squares (MSS)')
        plt.title('MSS Solution Quality Comparison')
        plt.xticks(x, scales)
        plt.legend()
        
        # Add labels on top of bars
        for i, val in enumerate(bf_mss):
            plt.text(i - width, val, f'{int(val)}', ha='center', va='bottom', fontsize=8, rotation=45)
        
        plt.tight_layout()
        output_mss = os.path.join(RESULTS_DIR, 'mss_accuracy_chart.png')
        plt.savefig(output_mss)
        print(f"Generated: {output_mss}")

    except Exception as e:
        print(f"Error generating charts: {e}")

if __name__ == "__main__":
    generate_charts()
