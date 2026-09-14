import numpy as np
from CoolProp.CoolProp import PropsSI


class RankineCycle:
    """
    Rankine Cycle: Ideal steam power cycle.
    Steps:
      1-2: Isentropic compression (pump)
      2-3: Constant-pressure heat addition (boiler)
      3-4: Isentropic expansion (turbine)
      4-1: Constant-pressure heat rejection (condenser)
    """

    def __init__(self, p_high=10.0, p_low=0.05, T_superheat=500,
                 working_fluid="water"):
        self.p_high = p_high
        self.p_low = p_low
        self.T_sh = T_superheat
        self.fluid = working_fluid
        self._calculate()

    def _calculate(self):
        p_high_mpa = self.p_high
        p_low_mpa = self.p_low

        h_f_low = PropsSI("H", "P", p_low_mpa * 1e6, "Q", 0.0, self.fluid) / 1000
        s_f_low = PropsSI("S", "P", p_low_mpa * 1e6, "Q", 0.0, self.fluid) / 1000
        h_fg_low = (PropsSI("H", "P", p_low_mpa * 1e6, "Q", 1.0, self.fluid) -
                    PropsSI("H", "P", p_low_mpa * 1e6, "Q", 0.0, self.fluid)) / 1000

        h_1 = h_f_low
        s_1 = s_f_low

        s_2 = s_1
        h_2 = PropsSI("H", "S", s_2 * 1000, "P", p_high_mpa * 1e6, self.fluid) / 1000 + h_f_low
        h_2 = PropsSI("H", "S", s_2 * 1000, "P", p_high_mpa * 1e6, self.fluid) / 1000
        v_f_low = PropsSI("V", "P", p_low_mpa * 1e6, "Q", 0.0, self.fluid) / 1000
        w_pump = v_f_low * (p_high_mpa - p_low_mpa)
        h_2 = h_1 + w_pump

        h_3 = PropsSI("H", "T", self.T_sh + 273.15, "P", p_high_mpa * 1e6, self.fluid) / 1000
        s_3 = PropsSI("S", "T", self.T_sh + 273.15, "P", p_high_mpa * 1e6, self.fluid) / 1000

        s_4 = s_3
        h_4 = PropsSI("H", "S", s_4 * 1000, "P", p_low_mpa * 1e6, self.fluid) / 1000

        q_in = h_3 - h_2
        q_out = h_4 - h_1
        w_turb = h_3 - h_4
        w_pump_calc = h_2 - h_1
        w_net = w_turb - w_pump_calc
        self.eta_th = w_net / q_in

        if h_4 > PropsSI("H", "P", p_low_mpa * 1e6, "Q", 1.0, self.fluid) / 1000:
            x_4 = 1.0
        else:
            x_4 = (h_4 - PropsSI("H", "P", p_low_mpa * 1e6, "Q", 0.0, self.fluid) / 1000) / h_fg_low
        self.x_4 = x_4

        self.states = {
            "1": {"T": PropsSI("T", "P", p_low_mpa * 1e6, "Q", 0.0, self.fluid) - 273.15,
                  "P": p_low_mpa, "s": s_1, "h": h_1, "phase": "saturated_liquid"},
            "2": {"T": PropsSI("T", "P", p_high_mpa * 1e6, "Q", 0.0, self.fluid) - 273.15,
                  "P": p_high_mpa, "s": s_2, "h": h_2, "phase": "compressed_liquid"},
            "3": {"T": self.T_sh, "P": p_high_mpa, "s": s_3, "h": h_3, "phase": "superheated"},
            "4": {"T": PropsSI("T", "P", p_low_mpa * 1e6, "Q", 0.0, self.fluid) - 273.15,
                  "P": p_low_mpa, "s": s_4, "h": h_4, "phase": f"wet (x={x_4:.3f})"},
        }
        self.results = {
            "q_in": q_in,
            "q_out": q_out,
            "w_net": w_net,
            "w_turb": w_turb,
            "w_pump": w_pump_calc,
            "eta_th": self.eta_th,
            "p_high": p_high_mpa,
            "p_low": p_low_mpa,
            "T_sh": self.T_sh,
            "x_4": x_4,
        }

    def print_results(self):
        r = self.results
        print("=" * 55)
        print("         RANKINE CYCLE RESULTS")
        print("=" * 55)
        print(f"  High Pressure        : {r['p_high']:.2f} MPa")
        print(f"  Low Pressure         : {r['p_low']:.4f} MPa")
        print(f"  Superheat Temp       : {r['T_sh']:.1f} C")
        print(f"  Thermal Efficiency   : {r['eta_th']*100:.2f} %")
        print(f"  q_in                 : {r['q_in']:.2f} kJ/kg")
        print(f"  q_out                : {r['q_out']:.2f} kJ/kg")
        print(f"  W_turbine            : {r['w_turb']:.2f} kJ/kg")
        print(f"  W_pump               : {r['w_pump']:.2f} kJ/kg")
        print(f"  W_net                : {r['w_net']:.2f} kJ/kg")
        print(f"  Steam Quality (x4)   : {r['x_4']:.4f}")
        print("-" * 55)
        for i in ["1", "2", "3", "4"]:
            s = self.states[i]
            print(f"  State {i}: T={s['T']:.2f} C, P={s['P']:.4f} MPa, s={s['s']:.4f} kJ/(kg*K), h={s['h']:.4f} kJ/kg, {s['phase']}")
        print("=" * 55)

    def get_t_s_data(self, n_points=200):
        s_vals = np.linspace(self.states["1"]["s"] - 2, self.states["3"]["s"] + 2, n_points)
        p_vals = np.linspace(self.p_low, self.p_high, 50)
        return s_vals, None
