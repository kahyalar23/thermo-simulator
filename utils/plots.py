import numpy as np
import matplotlib.pyplot as plt

from cycles.carnot import CarnotCycle
from cycles.brayton import BraytonCycle
from cycles.rankine import RankineCycle


def plot_ts_diagram(cycle, title=None, save_path=None):
    if title is None:
        title = f"{type(cycle).__name__} - T-s Diagram"

    fig, ax = plt.subplots(figsize=(8, 6))

    if isinstance(cycle, CarnotCycle):
        T_H, T_C = cycle.T_H, cycle.T_C
        s1 = cycle.states["1"]["s"]
        s2 = cycle.states["2"]["s"]
        s3 = cycle.states["3"]["s"]
        s4 = cycle.states["4"]["s"]
        s_min = min(s1, s2, s3, s4) - 0.5
        s_max = max(s1, s2, s3, s4) + 0.5

        ax.plot([s1, s2], [T_H, T_H], "b-", lw=2, label="1-2: Isothermal Heat Add.")
        ax.plot([s2, s3], [T_H, T_C], "r-", lw=2, label="2-3: Isentropic Expansion")
        ax.plot([s3, s4], [T_C, T_C], "b-", lw=2, label="3-4: Isothermal Heat Rej.")
        ax.plot([s4, s1], [T_C, T_H], "r-", lw=2, label="4-1: Isentropic Compression")
        ax.fill_between([s4, s3, s2, s1], [T_C, T_C, T_H, T_H], alpha=0.15, color="orange")
        ax.set_xlim(s_min, s_max)

    elif isinstance(cycle, BraytonCycle):
        s1 = cycle.states["1"]["s"]
        s2 = cycle.states["2"]["s"]
        s3 = cycle.states["3"]["s"]
        s4 = cycle.states["4"]["s"]

        ax.plot([s1, s2], [cycle.T_1, cycle.T_2], "b-", lw=2, label="1-2: Isentropic Comp.")
        ax.plot([s2, s3], [cycle.T_2, cycle.T_3], "r-", lw=2, label="2-3: Const-P Heat Add.")
        ax.plot([s3, s4], [cycle.T_3, cycle.T_4], "b-", lw=2, label="3-4: Isentropic Exp.")
        ax.plot([s4, s1], [cycle.T_4, cycle.T_1], "r-", lw=2, label="4-1: Const-P Heat Rej.")
        ax.fill_between([s4, s3, s2, s1], [cycle.T_4, cycle.T_3, cycle.T_2, cycle.T_1], alpha=0.15, color="orange")

    elif isinstance(cycle, RankineCycle):
        s1 = cycle.states["1"]["s"]
        s2 = cycle.states["2"]["s"]
        s3 = cycle.states["3"]["s"]
        s4 = cycle.states["4"]["s"]

        ax.plot([s1, s2], [cycle.states["1"]["T"], cycle.states["2"]["T"]], "b-", lw=2, label="1-2: Pump")
        ax.plot([s2, s3], [cycle.states["2"]["T"], cycle.states["3"]["T"]], "r-", lw=2, label="2-3: Boiler")
        ax.plot([s3, s4], [cycle.states["3"]["T"], cycle.states["4"]["T"]], "b-", lw=2, label="3-4: Turbine")
        ax.plot([s4, s1], [cycle.states["4"]["T"], cycle.states["1"]["T"]], "r-", lw=2, label="4-1: Condenser")
        ax.fill_between([s4, s3, s2, s1], [cycle.states["4"]["T"], cycle.states["3"]["T"], cycle.states["2"]["T"], cycle.states["1"]["T"]], alpha=0.15, color="orange")

    else:
        ax.text(0.5, 0.5, "Invalid cycle", transform=ax.transAxes, ha="center")

    ax.set_xlabel("Entropy (kJ/(kg*K))", fontsize=12)
    ax.set_ylabel("Temperature (K)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=10)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_pv_diagram(cycle, title=None, save_path=None):
    if title is None:
        title = f"{type(cycle).__name__} - P-v Diagram"

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.text(0.5, 0.5, "P-v Diagram\n(TODO: Phase curve)", transform=ax.transAxes, ha="center", fontsize=14)
    ax.set_xlabel("Specific Volume (m3/kg)", fontsize=12)
    ax.set_ylabel("Pressure (MPa)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=10)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_cycle_comparison(cycles, titles=None, save_path=None):
    if titles is None:
        titles = [type(c).__name__ for c in cycles]

    n = len(cycles)
    fig, axes = plt.subplots(1, n, figsize=(7 * n, 5))
    if n == 1:
        axes = [axes]

    for ax, cycle, t in zip(axes, cycles, titles):
        if isinstance(cycle, CarnotCycle):
            T_H, T_C = cycle.T_H, cycle.T_C
            s1, s2, s3, s4 = (cycle.states[k]["s"] for k in ["1", "2", "3", "4"])
            ax.plot([s1, s2], [T_H, T_H], "b-", lw=2)
            ax.plot([s2, s3], [T_H, T_C], "r-", lw=2)
            ax.plot([s3, s4], [T_C, T_C], "b-", lw=2)
            ax.plot([s4, s1], [T_C, T_H], "r-", lw=2)
            ax.fill_between([s4, s3, s2, s1], [T_C, T_C, T_H, T_H], alpha=0.15, color="orange")
            ax.set_title(f"{t}\neta={cycle.eta_th*100:.1f}%", fontsize=11)
        elif isinstance(cycle, BraytonCycle):
            s1, s2, s3, s4 = (cycle.states[k]["s"] for k in ["1", "2", "3", "4"])
            ax.plot([s1, s2], [cycle.T_1, cycle.T_2], "b-", lw=2)
            ax.plot([s2, s3], [cycle.T_2, cycle.T_3], "r-", lw=2)
            ax.plot([s3, s4], [cycle.T_3, cycle.T_4], "b-", lw=2)
            ax.plot([s4, s1], [cycle.T_4, cycle.T_1], "r-", lw=2)
            ax.fill_between([s4, s3, s2, s1], [cycle.T_4, cycle.T_3, cycle.T_2, cycle.T_1], alpha=0.15, color="orange")
            ax.set_title(f"{t}\neta={cycle.eta_th*100:.1f}%", fontsize=11)
        elif isinstance(cycle, RankineCycle):
            s1, s2, s3, s4 = (cycle.states[k]["s"] for k in ["1", "2", "3", "4"])
            ax.plot([s1, s2], [cycle.states["1"]["T"], cycle.states["2"]["T"]], "b-", lw=2)
            ax.plot([s2, s3], [cycle.states["2"]["T"], cycle.states["3"]["T"]], "r-", lw=2)
            ax.plot([s3, s4], [cycle.states["3"]["T"], cycle.states["4"]["T"]], "b-", lw=2)
            ax.plot([s4, s1], [cycle.states["4"]["T"], cycle.states["1"]["T"]], "r-", lw=2)
            ax.fill_between([s4, s3, s2, s1], [cycle.states["4"]["T"], cycle.states["3"]["T"], cycle.states["2"]["T"], cycle.states["1"]["T"]], alpha=0.15, color="orange")
            ax.set_title(f"{t}\neta={cycle.eta_th*100:.1f}%", fontsize=11)

        ax.set_xlabel("Entropy (kJ/(kg*K))")
        ax.set_ylabel("Temperature (K)")
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=9)

    plt.suptitle("Thermodynamic Cycle Comparison", fontsize=16, fontweight="bold")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
