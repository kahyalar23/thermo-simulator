import argparse
import sys
import os
import io
import locale

# Force UTF-8 output for Turkish characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
os.environ["PYTHONIOENCODING"] = "utf-8"

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cycles.carnot import CarnotCycle
from cycles.brayton import BraytonCycle
from cycles.rankine import RankineCycle
from utils.plots import plot_ts_diagram, plot_pv_diagram, plot_cycle_comparison


def run_carnot(args):
    cycle = CarnotCycle(T_hot_K=args.T_hot, T_cold_K=args.T_cold)
    cycle.print_results()
    plot_ts_diagram(cycle, save_path="carnot_ts.png")
    plot_pv_diagram(cycle, save_path="carnot_pv.png")
    return cycle


def run_brayton(args):
    cycle = BraytonCycle(T_inlet=args.T_in, T_max=args.T_max, pressure_ratio=args.pr)
    cycle.print_results()
    plot_ts_diagram(cycle, save_path="brayton_ts.png")
    plot_pv_diagram(cycle, save_path="brayton_pv.png")
    return cycle


def run_rankine(args):
    cycle = RankineCycle(p_high=args.p_high, p_low=args.p_low, T_superheat=args.T_sh)
    cycle.print_results()
    plot_ts_diagram(cycle, save_path="rankine_ts.png")
    plot_pv_diagram(cycle, save_path="rankine_pv.png")
    return cycle


def main():
    parser = argparse.ArgumentParser(
        description="Thermodynamic Cycle Simulator - ITU Civil & Mechanical"
    )
    parser.add_argument("--cycle", type=str, default="all",
                        choices=["carnot", "brayton", "rankine", "all"],
                        help="Cycle to compute")
    parser.add_argument("--T_hot", type=float, default=800, help="Carnot hot source K")
    parser.add_argument("--T_cold", type=float, default=300, help="Carnot cold sink K")
    parser.add_argument("--T_in", type=float, default=300, help="Brayton inlet temp K")
    parser.add_argument("--T_max", type=float, default=1200, help="Brayton max temp K")
    parser.add_argument("--pr", type=float, default=10, help="Pressure ratio")
    parser.add_argument("--p_high", type=float, default=10, help="Rankine high pressure MPa")
    parser.add_argument("--p_low", type=float, default=0.05, help="Rankine low pressure MPa")
    parser.add_argument("--T_sh", type=float, default=500, help="Rankine superheat C")
    parser.add_argument("--compare", action="store_true", help="Compare all cycles")
    parser.add_argument("--no_plot", action="store_true", help="Skip plots")
    parser.add_argument("--debug", action="store_true", help="Debug mode: show full state data")

    args = parser.parse_args()

    cycles = []
    names = []

    if args.cycle in ["carnot", "all"]:
        print("=" * 60)
        print("  CARNOT CYCLE RESULTS")
        print("=" * 60)
        c = run_carnot(args)
        cycles.append(c); names.append("Carnot")

    if args.cycle in ["brayton", "all"]:
        print("\n" + "=" * 60)
        print("  BRAYTON CYCLE RESULTS")
        print("=" * 60)
        b = run_brayton(args)
        cycles.append(b); names.append("Brayton")

    if args.cycle in ["rankine", "all"]:
        print("\n" + "=" * 60)
        print("  RANKINE CYCLE RESULTS")
        print("=" * 60)
        r = run_rankine(args)
        cycles.append(r); names.append("Rankine")

    if args.compare and len(cycles) > 1:
        print("\n" + "=" * 60)
        print("  CYCLE COMPARISON")
        print("=" * 60)
        plot_cycle_comparison(cycles, titles=names, save_path="comparison.png")

    if not args.no_plot:
        print("\n[T-s and P-v diagrams saved.]")
        print("   (carnot_ts.png, carnot_pv.png, etc.)")

    if args.debug:
        print("\n" + "=" * 60)
        print("  DEBUG MODE - FULL STATE DATA")
        print("=" * 60)
        for cycle in cycles:
            print(f"\n--- {type(cycle).__name__} ---")
            print(f"  eta_th = {cycle.eta_th*100:.4f}%")
            for k in ["1", "2", "3", "4"]:
                s = cycle.states[k]
                print(f"  State {k}: T={s.get('T')}, P={s.get('P')}, s={s.get('s')}, h={s.get('h')}")
            print(f"  Results: {cycle.results}")

    print("\n[DONE.]")


if __name__ == "__main__":
    main()
