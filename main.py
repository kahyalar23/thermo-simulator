import argparse
import sys
import os

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
        description="Termodinamik Cevrim Simulatoru - ITU IC & Makine"
    )
    parser.add_argument("--cycle", type=str, default="all",
                        choices=["carnot", "brayton", "rankine", "all"],
                        help="Hesaplanacak çevrim")
    parser.add_argument("--T_hot", type=float, default=800, help="Carnot sıcak kaynak K")
    parser.add_argument("--T_cold", type=float, default=300, help="Carnot sıcak sönük K")
    parser.add_argument("--T_in", type=float, default=300, help="Brayton giriş sıcaklığı K")
    parser.add_argument("--T_max", type=float, default=1200, help="Brayton maksimum sıcaklık K")
    parser.add_argument("--pr", type=float, default=10, help="Basınç oranı")
    parser.add_argument("--p_high", type=float, default=10, help="Rankine yüksek basınç MPa")
    parser.add_argument("--p_low", type=float, default=0.05, help="Rankine düşük basınç MPa")
    parser.add_argument("--T_sh", type=float, default=500, help="Aşırı isıtma sıcaklığı °C")
    parser.add_argument("--compare", action="store_true", help="Tüm çevrimleri karşılaştır")
    parser.add_argument("--no_plot", action="store_true", help="Diagramları gösterme")

    args = parser.parse_args()

    cycles = []
    names = []

    if args.cycle in ["carnot", "all"]:
        print("\n" + "=" * 60)
        print("  CARNOT ÇEVRİMİ İÇİN HESAPLAMA")
        print("=" * 60)
        c = run_carnot(args)
        cycles.append(c); names.append("Carnot")

    if args.cycle in ["brayton", "all"]:
        print("\n" + "=" * 60)
        print("  BRAYTON ÇEVRİMİ İÇİN HESAPLAMA")
        print("=" * 60)
        b = run_brayton(args)
        cycles.append(b); names.append("Brayton")

    if args.cycle in ["rankine", "all"]:
        print("\n" + "=" * 60)
        print("  RANKINE ÇEVRİMİ İÇİN HESAPLAMA")
        print("=" * 60)
        r = run_rankine(args)
        cycles.append(r); names.append("Rankine")

    if args.compare and len(cycles) > 1:
        print("\n" + "=" * 60)
        print("  ÇEVRİM KARŞILAŞTIRMASI")
        print("=" * 60)
        plot_cycle_comparison(cycles, titles=names, save_path="comparison.png")

    if not args.no_plot:
        print("\n[T-s ve P-v diagramlari kaydedildi.]")
        print("   (carnot_ts.png, carnot_pv.png, vb.)")

    print("\n[Islem tamamlandi.]")


if __name__ == "__main__":
    main()
