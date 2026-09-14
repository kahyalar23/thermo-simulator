import pytest
from cycles.carnot import CarnotCycle
from cycles.brayton import BraytonCycle
from cycles.rankine import RankineCycle


class TestCarnotCycle:
    def test_efficiency(self):
        c = CarnotCycle(T_hot_K=600, T_cold_K=300)
        assert abs(c.eta_th - 0.5) < 1e-6

    def test_cold_equals_hot(self):
        with pytest.raises(ValueError):
            CarnotCycle(T_hot_K=300, T_cold_K=300)

    def test_cold_above_hot(self):
        with pytest.raises(ValueError):
            CarnotCycle(T_hot_K=300, T_cold_K=600)

    def test_states_have_properties(self):
        c = CarnotCycle(T_hot_K=800, T_cold_K=300)
        for i in ["1", "2", "3", "4"]:
            assert "T" in c.states[i]
            assert "P" in c.states[i]
            assert "s" in c.states[i]
            assert "h" in c.states[i]

    def test_w_net_positive(self):
        c = CarnotCycle(T_hot_K=800, T_cold_K=300)
        assert c.results["w_net"] > 0


class TestBraytonCycle:
    def test_efficiency_ideal(self):
        b = BraytonCycle(T_inlet=300, T_max=1200, pressure_ratio=10)
        expected = 1 - (1 / 10 ** ((1.4 - 1) / 1.4))
        assert abs(b.eta_th - expected) < 0.01

    def test_temperatures_order(self):
        b = BraytonCycle(T_inlet=300, T_max=1200, pressure_ratio=10)
        assert b.T_2 > b.T_1
        assert b.T_3 > b.T_2
        assert b.T_3 > b.T_4
        assert b.T_4 > b.T_1

    def test_w_net_positive(self):
        b = BraytonCycle(T_inlet=300, T_max=1200, pressure_ratio=10)
        assert b.results["w_net"] > 0

    def test_higher_pr_higher_eff(self):
        b1 = BraytonCycle(T_inlet=300, T_max=1200, pressure_ratio=5)
        b2 = BraytonCycle(T_inlet=300, T_max=1200, pressure_ratio=15)
        assert b2.eta_th > b1.eta_th

    def test_states_have_properties(self):
        b = BraytonCycle(T_inlet=300, T_max=1200, pressure_ratio=10)
        for i in ["1", "2", "3", "4"]:
            assert "T" in b.states[i]
            assert "P" in b.states[i]


class TestRankineCycle:
    def test_efficiency_reasonable(self):
        r = RankineCycle(p_high=10.0, p_low=0.05, T_superheat=500)
        assert 0.2 < r.eta_th < 0.5

    def test_superheat_temp(self):
        r = RankineCycle(p_high=10.0, p_low=0.05, T_superheat=500)
        assert r.states["3"]["T"] == 500

    def test_pump_work_positive(self):
        r = RankineCycle(p_high=10.0, p_low=0.05, T_superheat=500)
        assert r.results["w_pump"] > 0

    def test_turbine_work_positive(self):
        r = RankineCycle(p_high=10.0, p_low=0.05, T_superheat=500)
        assert r.results["w_turb"] > 0

    def test_w_net_positive(self):
        r = RankineCycle(p_high=10.0, p_low=0.05, T_superheat=500)
        assert r.results["w_net"] > 0

    def test_q_in_positive(self):
        r = RankineCycle(p_high=10.0, p_low=0.05, T_superheat=500)
        assert r.results["q_in"] > 0

    def test_quality_below_one(self):
        r = RankineCycle(p_high=10.0, p_low=0.05, T_superheat=500)
        assert 0 < r.x_4 < 1.0

    def test_states_have_properties(self):
        r = RankineCycle(p_high=10.0, p_low=0.05, T_superheat=500)
        for i in ["1", "2", "3", "4"]:
            assert "T" in r.states[i]
            assert "P" in r.states[i]
            assert "s" in r.states[i]
            assert "h" in r.states[i]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
