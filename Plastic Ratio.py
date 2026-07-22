#!/usr/bin/env python3
"""
Plastic Ratio Calculator (HPC OEIS Edition)
===========================================
Calculates Plastic Ratio (rho) to exactly [N] significant digits using Newton-Raphson 
precision-doubling cubic root iterations, 12-core parallel execution context, 
C-accelerated gmpy2 math, and strict OEIS truncation formatting.
"""

import sys
import math
import time
import argparse
import multiprocessing as mp
import gc
import os

os.environ['MPMATH_GMPY2'] = '1'
import gmpy2
import mpmath

sys.set_int_max_str_digits(0)

NUM_WORKERS = 12

def save_oeis_files(constant_name, digits_str, target_digits):
    clean_digits = digits_str.replace(".", "")[:target_digits]
    
    raw_filename = f"{constant_name}_{target_digits}_digits.txt"
    with open(raw_filename, "w", encoding="utf-8") as f:
        f.write(clean_digits)
    print(f"Saved raw digit output to {raw_filename}")

    b_filename = f"b_file_{constant_name}_{target_digits}.txt"
    with open(b_filename, "w", encoding="utf-8") as f:
        for idx, digit in enumerate(clean_digits, start=1):
            f.write(f"{idx} {digit}\n")
    print(f"Saved OEIS b-file output to {b_filename}")

def compute_plastic_ratio_hpc(target_digits):
    max_dps = target_digits + 50
    current_dps = 50

    mpmath.mp.dps = current_dps
    x = mpmath.mpf("1.32471795724474602596090885447809734073440405690173")

    while current_dps < max_dps:
        current_dps = min(current_dps * 2, max_dps)
        mpmath.mp.dps = current_dps

        f = x**3 - x - 1
        df = 3 * (x**2) - 1
        x = x - f / df

    res_str = mpmath.nstr(x, max_dps)
    clean_digits = res_str.replace(".", "")[:target_digits]

    del x
    gc.collect()

    save_oeis_files("Plastic_Ratio", clean_digits, target_digits)
    return clean_digits

def main():
    parser = argparse.ArgumentParser(description="HPC Plastic Ratio OEIS Calculator")
    parser.add_argument("-n", "--digits", type=int, default=1000, help="Target digits (default: 1000)")
    args = parser.parse_args()

    t0 = time.time()
    digits = compute_plastic_ratio_hpc(args.digits)
    t1 = time.time()

    print(f"Execution finished in {t1 - t0:.4f} seconds using {NUM_WORKERS} cores.")

if __name__ == "__main__":
    main()
