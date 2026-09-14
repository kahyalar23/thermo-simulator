import numpy as np
from CoolProp.CoolProp import PropsSI


class BraytonCycle:
    """
    Brayton Cycle: Ideal gas turbine cycle.
    Steps:
      1-2: Isentropic compression (compressor)
      2-3: Constant-pressure heat addition (combustor)
      3-4: Isentropic expansion (turbine)
      4-1: Constant-pressure heat rejection (exhaust)
    """

    def __init__(self, T_inlet=300, T_max=1200, pressure_ratio=10,
                 working_fluid="air", gamma=1.4):
        self.T_1 = T_inlet
        self.T_3 = T_max
        self.rp = pressure_ratio
        self.fluid = working_fluid
        self.gamma = gamma
        self._calculate()

    def _calculate(self):
        R = 0.287 if self.fluid == "air" else 0.2968
        cp = R * self.gamma / (self.gamma - 1)
        cv = R / (self.gamma - 1)
        self.cp = cp

        self.eta_comp = 1.0
        self.eta_turb = 1.0

        self.T_2 = self.T_1 * self.rp ** ((self.gamma - 1) / self.gamma)
        self.T_4 = self.T_3 / self.rp ** ((self.gamma - 1) / self.gamma)

        self.w_comp = cp * (self.T_2 - self.T_1)
        self.w_turb = cp * (self.T_3 - self.T_4)
        self.w_net = self.w_turb - self.w_comp

        self.q_in = cp * (self.T_3 - self.T_2)
        self.q_out = cp * (self.T_4 - self.T_1)
        self.eta_th = self.w_net / self.q_in

        self.p_1 = 0.1
        self.p_2 = self.p_1 * self.rp
        self.p_3 = self.p_2
        self.p_4 = self.p_1

        self.states = {
            "1": {"T": self.T_1, "P": self.p_1, "s": 0.0, "h": cp * self.T_1},
            "2": {"T": self.T_2, "P": self.p_2, "s": 0.0, "h": cp * self.T_2},
            "3": {"T": self.T_3, "P": self.p_3, "s": self.q_in / self.T_3, "h": cp * self.T_3},
            "4": {"T": self.T_4, "P": self.p_4, "s": self.q_out / self.T_4, "h": cp * self.T_4},
        }
        self.results = {
            "q_in": self.q_in,
            "q_out": self.q_out,
            "w_net": self.w_net,
            "w_comp": self.w_comp,
            "w_turb": self.w_turb,
            "eta_th": self.eta_th,
            "T_1": self.T_1,
            "T_3": self.T_3,
            "pressure_ratio": self.rp,
            "cp": cp,
        }

    def print_results(self):
        r = self.results
        print("=" * 55)
        print("         BRAYTON CYCLE RESULTS")
        print("=" * 55)
        print(f"  Inlet Temp           : {r['T_1']:.1f} K")
        print(f"  Combustion Temp      : {r['T_3']:.1f} K")
        print(f"  Pressure Ratio       : {r['pressure_ratio']}")
        print(f"  Thermal Efficiency   : {r['eta_th']*100:.2f} %")
        print(f"  q_in                 : {r['q_in']:.2f} kJ/kg")
        print(f"  q_out                : {r['q_out']:.2f} kJ/kg")
        print(f"  W_compressor         : {r['w_comp']:.2f} kJ/kg")
        print(f"  W_turbine            : {r['w_turb']:.2f} kJ/kg")
        print(f"  W_net                : {r['w_net']:.2f} kJ/kg")
        print("-" * 55)
        for i in ["1", "2", "3", "4"]:
            s = self.states[i]
            print(f"  State {i}: T={s['T']:.1f} K, P={s['P']:.4f} MPa, s={s['s']:.4f} kJ/(kg*K), h={s['h']:.2f} kJ/kg")
        print("=" * 55)

    def get_t_s_data(self, n_points=200):
        s1 = self.states["1"]["s"]
        s3 = self.states["3"]["s"]
        s_vals = np.concatenate([
            np.linspace(s1 - 1, s1, n_points // 4),
            np.linspace(s1, s3, n_points // 4),
            np.linspace(s3, s3 + 0.5, n_points // 4),
            np.linspace(s3 + 0.5, s1 - 1, n_points // 4),
        ])
        t_vals = np.piecewise(s_vals, [
            s_vals <= s1,
            (s_vals > s1) & (s_vals <= s1),
            s_vals > s3,
            True
        ], [
            lambda s: self.T_1 * np.exp((s - s1) * 0),
            lambda s: self.T_3 * np.ones_like(s),
            lambda s: self.T_4 * np.exp((s - s3) * 0),
            lambda s: self.T_1 * np.ones_like(s),
        ])
        return s_vals, t_vals
