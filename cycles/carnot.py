import numpy as np
from CoolProp.CoolProp import PropsSI


class CarnotCycle:
    """
    Carnot Cycle: Ideal reversible cycle between two thermal reservoirs.
    Çalışma sıcaklığı: Argon (iyi gaz davranışı)
    Sabit özellikli ideal gaz yaklaşımı ile hesaplanır.
    Steps:
      1→2: Isothermal heat addition at T_H (expansion)
      2→3: Isentropic expansion (T_H → T_C)
      3→4: Isothermal heat rejection at T_C (compression)
      4→1: Isentropic compression (T_C → T_H)
    """

    def __init__(self, T_hot_K, T_cold_K, working_fluid="argon", p_min=0.1, p_max=10.0):
        self.T_H = T_hot_K
        self.T_C = T_cold_K
        self.fluid = working_fluid
        self.p_min = p_min
        self.p_max = p_max
        self._validate()
        self._calculate()

    def _validate(self):
        if self.T_H <= self.T_C:
            raise ValueError(f"T_hot ({self.T_H} K) must be > T_cold ({self.T_C} K)")
        if self.T_C <= 0:
            raise ValueError("T_cold must be > 0 K")

    def _calculate(self):
        self.eta_th = 1.0 - self.T_C / self.T_H

        R = PropsSI("GAS_CONSTANT", self.fluid) / 39.948
        cp = 0.5203 if self.fluid == "argon" else 0.718
        cv = cp - R
        gamma = cp / cv

        p1 = self.p_max
        p2 = self.p_min
        p3 = self.p_min
        p4 = self.p_max

        T1 = self.T_H
        T2 = self.T_H
        T3 = self.T_C
        T4 = self.T_C

        s1 = 0.0
        s2 = s1 + R * np.log(p1 / p2)
        s3 = s2
        s4 = s3 + R * np.log(p3 / p4)

        h1 = cp * T1
        h2 = cp * T2
        h3 = cp * T3
        h4 = cp * T4

        q_in = self.T_H * (s2 - s1)
        q_out = self.T_C * (s3 - s4)
        w_net = q_in - q_out
        w_comp = h4 - h3
        w_turb = h1 - h2

        self.cp = cp
        self.R = R

        self.states = {
            "1": {"T": T1, "P": p1, "s": s1, "h": h1, "phase": "gas"},
            "2": {"T": T2, "P": p2, "s": s2, "h": h2, "phase": "gas"},
            "3": {"T": T3, "P": p3, "s": s3, "h": h3, "phase": "gas"},
            "4": {"T": T4, "P": p4, "s": s4, "h": h4, "phase": "gas"},
        }
        self.results = {
            "q_in": q_in,
            "q_out": q_out,
            "w_net": w_net,
            "w_turb": w_turb,
            "w_comp": w_comp,
            "eta_th": self.eta_th,
            "T_H": self.T_H,
            "T_C": self.T_C,
        }

    def print_results(self):
        r = self.results
        print("=" * 55)
        print("         CARNOT CYCLE RESULTS")
        print("=" * 55)
        print(f"  Hot Source Temp      : {r['T_H']:.1f} K")
        print(f"  Cold Sink Temp       : {r['T_C']:.1f} K")
        print(f"  Thermal Efficiency   : {r['eta_th']*100:.2f} %")
        print(f"  q_in (heat input)    : {r['q_in']:.2f} kJ/kg")
        print(f"  q_out (heat output)  : {r['q_out']:.2f} kJ/kg")
        print(f"  W_net (net work)     : {r['w_net']:.2f} kJ/kg")
        print(f"  W_turbine            : {r['w_turb']:.2f} kJ/kg")
        print(f"  W_compressor         : {r['w_comp']:.2f} kJ/kg")
        print(f"  Working Fluid        : {self.fluid}")
        print("-" * 55)
        for i in ["1", "2", "3", "4"]:
            s = self.states[i]
            print(f"  State {i}: T={s['T']:.1f} K, P={s['P']:.4f} MPa, s={s['s']:.4f} kJ/(kg*K), h={s['h']:.4f} kJ/kg")
        print("=" * 55)

    def get_t_s_data(self, n_points=200):
        s_vals = np.linspace(self.states["4"]["s"] - 2, self.states["1"]["s"] + 2, n_points)
        t_carnot = np.where(s_vals > self.states["1"]["s"], self.T_H, self.T_C)
        return s_vals, t_carnot
